---
layout: guide
title: SMART - REST App Tutorial
---

# SMART REST App Tutorial

For many apps you may want to build the [SMART Connect JavaScript
library](/guide/tutorials/smart_connect.html) will be the only interface you
will need to get the data you require from a SMART container. But if your app
has a backend that needs access to the data as well, you will need to use the
SMART REST API. This tutorial will show you how to setup and use the REST API
to enable that type of "server-to-server" data flow.


## Authentication and Authorization is Required

With SMART Connect authentication and authorization are handled for you by the
SMART Connect library and the SMART Container. Specifically, the JS API call
notified the outer frame (supplied by the SMART Container) of the data
request, and the outer frame already knows the identity of the logged in user
and what medical record currently being accessed. Authentication and
authorization of that request happened inside the user's browser without any
effort required of you as the app writer.

Now consider a case where you want the backend of your app to obtain data
directly from the SMART Container. In this case, the SMART Container doesn't
know in advance who is making the call and what data they are authorized to
access. The calls the backend of your app makes must contain information that
proves to the Container they come from a trusted and authenticated source.


## Choosing the Right Tools

You can write a SMART REST app in many languages and frameworks so you have
great flexibility in choosing the tools you work with. Generally, you'll want
to look for a language with existing [OAuth][] libraries to handle the details
of signing requests to the SMART container.

We'll illustrate the highlights of the REST API with a simple Python-based
SMART app called (unimaginatively) [smart_rest_minimal][]. This app is written
using the excellent [Flask][] web microframework. This isn't a tutorial on
Flask, but to get started all you'll need to understand is that Flask provides
a simple mechanism to map HTTP URLs to Python functions.

[smart_rest_minimal]: https://github.com/chb/smart_sample_apps/tree/master/rest_minimal
[flask]: http://flask.pocoo.org/


## Getting to Know OAuth

To authenticate your apps' calls to the SMART Container, SMART uses [OAuth][],
an open standard for access delegation.

[oauth]: http://tools.ietf.org/html/rfc5849

OAuth bundles two features essential in using SMART REST:

1. A way to label and sign HTTP requests using an identifier token and a secret
   string

2. A dance involving the user's browser, the data server, and the server that
   wishes to consume the data, which, when the user approves the exchange,
   provides the data consumer with the token and secret needed to perform the
   authenticated API calls as per (1).

SMART employs both (1) the signing features of OAuth and (2) the full OAuth
authentication "dance".

## OAuth Authentication Flow Visualized

[Here](http://developer.yahoo.com/oauth/guide/oauth-auth-flow.html) is a
diagram of the OAuth 1.0 flow for visual learners. SMART REST apps _must_
perform the standard OAuth 1.0a dance including providing authorization
callback URLs.


## Important: Change Your Consumer Secret in Production!

Each SMART container your app runs against must first "install" your app by
inserting your app's manifest into it's database. This data includes your app's
OAuth `consumer-secret` which is the shared secret between your app and the
container that __ALL SECURITY__ of your app's communication with the server
relies on and is a basic requirement of OAuth-signed REST API calls.

<div id='consumer_secret_warning' class='red_box'>
  If this secret is revealed to or guessed by a 3rd party, the security of
  your app and the container has been breached! Using the default secret
  ("smartapp-secret") while in development is acceptable, but:
  <br />
  <br />
  <strong>
    <em>
      YOU MUST CHANGE THE <code>consumer-secret</code> IN PRODUCTION!
    <br />
    </em>
  </strong>
</div>

This secret is provisioned when your app is loaded into the smart container with
the following command:

    $ manage.py load_app <manifest-location> <secret>


## The "Minimal" SMART REST App

The code for the [here][] for you to follow along. It is a
single python file and we'll start from the top and work our way down
explaining the code as we go.

[here]: https://github.com/chb/smart_sample_apps/blob/master/rest_minimal/wsgi.py


### Import the SMARTClient

First, we import the `flask`, `logging` and the SMART Python client into the
app:

    import flask
    import logging
    from smart_client.client import SMARTClient


### Configure the OAuth "Endpoint"

Next we set up an object that contains all the information needed to talk to
the Container with OAuth.

    # SMART Container OAuth Endpoint Configuration
    _ENDPOINT = {
        "url": "http://sandbox-api-v06.smartplatforms.org",
        "name": "SMART Sandbox API v0.6",
        "app_id": "my-app@apps.smartplatforms.org",
        "consumer_key": "my-app@apps.smartplatforms.org",
        "consumer_secret": "smartapp-secret"
    }


### Configure Flask

After that comes a few lines of configuration for Flask:

    # Other Configuration (you shouldn't need to change this)
    logging.basicConfig(level=logging.DEBUG)  # cf. .INFO; default is WARNING
    application = app = flask.Flask(  # Some PaaS need "application"
        'wsgi',
        template_folder='app',
        static_folder='app/static',
        static_url_path='/static'
    )
    app.debug = True
    app.secret_key = 'mySMARTrestAPPrules!!'  # only for encrypting the session


### Some Helper Functions

In the next section comes four internal helper functions for the OAuth and
SMARTClient. (Internal helper functions and variables are indicated with a
leading underscore.). We'll come back to them as they are used below.


## The /index Route

We designed this app to handle most of the typical use cases for SMART REST,
therefore it's not as simple as it could possibily be. These use cases include
showing the user a record selection page and record change within the app.
This adds much of the extra complexity, however we think the extra complexity
is worth it since this code can be used the basis for your real-world REST
app.

The `index` function is the core of the app. It responds to both the `/index`
and `/smartapp/index.html` URLs. The second URL is the default URL used by the
SMART reference Container's "MyApp" app.


### Setting up api_base and record_id

First, we define `api_base` as the Container URL we set before in `_ENDPOINT`
and save it in Flask's session storage:

    api_base = flask.session['api_base'] = _ENDPOINT.get('url')

Next we check if we already have a `record_id` in the session store. This is
not needed in trivial cases, but for real apps that may want to switch between
records it's required:

    current_record_id = flask.session.get('record_id')
    args_record_id = flask.request.args.get('record_id')


### Conditional Redirect to Record Selection

If we didn't get a `record_id` in the arguments of the URL (`args_record_id`),
we need to redirect the user to a record selection UI. The URL for this UI is
the `launch_url` and is a property of the client (`client.launch_url`). If it
is found, we redirect to it here. (We'll describe the `init_smart_client()`
call shortly.)

        logging.debug('Redirecting to app launch_url: ' + client.launch_url)
        return flask.redirect(client.launch_url)

Once the user has selected a record, it will return to the `index` URL above,
now sending the `record_id` as an URL argument.


### Check for Record Switch

The next section is some housekeeping that checks if the passed in `record_id`
is different from the `record_id` saved in the Flask session. If it is, we've
had a record switch and need to update our session information.


### Initialize the SMARTClient

Now we can initialize the client with the line:

    client = _init_smart_client(record_id)

`_init_smart_client()`, simply wraps the call initalizing the SMARTClient in a
`try/expect` block so that any errors thrown by the client will be logged and
handled appropriately. Note that a valid `record_id` is not needed to
initalize the client. This is to support the use case where you don't know in
advance the record you want to access and you want your user to be presented
with a UI for selecting a record. This is used in the `if not args_record_id`
block.


### Requesting the Request Token

The next line, checks to see if we already have an OAuth access token:

    acc_token = flask.session.get('acc_token')

That can happen if the user just switched records. We'll assume the default
case of no access token.

Next we call a helper function to get the OAuth request token, which is the
first step in the OAuth "dance", with the call:

        _request_token_for_record(client)

See step (2) in the [Yahoo OAuth
diagram](http://developer.yahoo.com/oauth/guide/oauth-auth-flow.html).

If there were no errors in fetching the request token from the Container, this
helper function saves the returned token in the Flask session store with the
line:

        flask.session['req_token'] = client.fetch_request_token()


### User Authorization for Access

The next step in the OAuth dance is to have the user signal to the container
that they approve this app's request for access. This corresponds to step (3)
in the diagram. How does the user apporove this request for access? You app
redirects the user's browser to the container's "access authorization page"
defined in the SMARTClient:

     flask.redirect(smart.auth_redirect_url)


### Exchange the Request Token for the Access Token

Once the user authorizes your app's request with the container, the container
will redirect the users' browser to the `oauth_callback` URL (typically
`/authorized`) that you defined in the manifest that you installed with the
container and the container passes an `oauth_verifer` as a HTTP parameter to
your page.

Your app's handler for this URL must then "exchange" the `request_token` and
the `oauth_verifer` (a temporary token) with the container to receive the
`access_token`. Once the `access_token` is received, the OAuth dance is
complete and your app can now access protected data until the access token
expires.

After a couple lines of code checking to make sure that we have the correct
tokens, the code makes this call to the `_exchange_token(verifier)` helper
function passing in the `oauth_verifer` send in the HTTP request arguments:

    _exchange_token(flask.request.args.get('oauth_verifier'))

Inside the helper function, this call performs the verifier for access token
exchange:

    acc_token = client.exchange_token(verifier)

If that proceded without error, control returns to the `authorize()` function,
which then redirects the user's browser back to `/index`. With the access
token saved in the Flask session, we can now access the data:

    return flask.redirect('/smartapp/index.html?api_base=%s&record_id=%s' %
                          (api_base, record_id))


### Accessing Protected Data With the Access Token


Now accessing data using the SMART REST API is simply a matter of
making calls such as:


    # Now we're ready to get data!
    # Let's fetch demographics and display the name
    demo = smart.get_demographics()


The result is an SMARTResponse object containing an RDF graph of data,
which we can query for just the fields we want which you can query with
SPARQL e.g.:

    sparql = """
        PREFIX vc: <http://www.w3.org/2006/vcard/ns#>
        SELECT ?given ?family
        WHERE {
            [] vc:n ?vcard .
            OPTIONAL { ?vcard vc:given-name ?given . }
            OPTIONAL { ?vcard vc:family-name ?family . }
        }
    """
    results = demo.graph.query(sparql)
    record_name = 'Unknown'
    if len(results) > 0:
        res = list(results)[0]
        record_name = '%s %s' % (res[0], res[1])

And that's it! You now have the ability to create apps that access SMART
Container via the REST API and so can work with records outside of the
Container's web UI allowing the creating of mobile and server apps!

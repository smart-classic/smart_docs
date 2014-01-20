---
layout: guide
title: SMART - REST App Tutorial
---

# SMART REST App Tutorial

For browser-based apps, the [SMART Connect JavaScript
library](/guide/tutorials/smart_connect.html) will often be the only interface
you need to fetch clinical data from a SMART container. But if your app runs
outside of the browser (for example, a native smartphone app), or if it has a
server-side backend that needs access to patient data, then the SMART REST API
can help. This tutorial will show you how to use the REST API to talk to a
SMART Container.


## Authentication and Authorization is Required

With SMART Connect, authentication and authorization are handled for you by the
SMART Connect library and the SMART Container. Specifically, the JS API call
notifies the outer frame (supplied by the SMART Container) of the data
request, and the outer frame already knows the identity of the logged in user
and what medical record currently being accessed. Authentication and
authorization of that request happen inside the user's browser without any
effort required on the part of the app developer.

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

OAuth provides a way for apps to obtain access tokens representing
narrow, user authorization decisions. For example, a token might represent
the fact that Dr. Dave has authorized the BP Centiles app to access
the record of Patient Penny. A SMART app signs each REST API call
with an appropriate access token, allowing the SMART Container to
authenticate access, confirm authorization, and return the appropriate
content.

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

We have a ["minimal" SMART REST][rest_minimal] example app that you can use as
a starting point. It is a single Python file and we'll start from the top and
work our way down explaining the code as we go.

[rest_minimal]: https://github.com/chb/smart_sample_apps/blob/master/rest_minimal/wsgi.py


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


For this app we hardcode the endpoint information for one container which is
the typical use case. However, an app can connect to multiple containers i.e.
endpoints aren't required to be hardcoded. For some use cases, it may be
useful to show a friendly list of containers to the user then use the endpoint
information of the container selected.


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


### The /index Route

We designed this app to handle most of the typical use cases for SMART REST,
therefore it's not as simple as it could possibly be. These use cases include
showing the user a record selection page and record change within the app.
This adds some extra complexity to the code, but we think this extra
complexity is worth it since this code can be used the basis for your
real-world REST app.

The `index` function is the core of the app. It responds to both the `/index`
and `/smartapp/index.html` URLs. The second URL is the default URL used by the
SMART reference Container's "MyApp" app.


### Get `record_id` or Redirect to Record Selection

First, we get the `record_id` from the HTTP request. It should be passed to
this function in the default app launch scenario, but it may not be passed in
all situations, so we must check for its existence. If it's missing from the
request we don't know what record we're trying to access and, therefore, we'll
need to redirect the user's browser to a record selection UI.

The URL for the record selection UI is the `launch_url` property of the client
(`client.launch_url`). If it is found, we redirect to it. (We'll describe the
`init_smart_client()` call shortly.)

    if not record_id:
        # no record_id, redirect to record selection page
        flask.session['sessions'] = {}
        client = _init_smart_client()  # just init to get launch_url
        assert client.launch_url, "No launch_url found in client. Aborting."
        logging.debug('Redirecting to app launch_url: %s', client.launch_url)
        return flask.redirect(client.launch_url)

Once the user has selected a record, it will return to the `index` URL above,
now sending the `record_id` as an URL argument.


### Check for a Valid Access Token

The next 35 lines or so are a series of tests to check if there is:

1. a valid `sessions` dictionary stored in the flask session cookie
2. a valid `session` dictionary for this `record_id` stored in the `sessions`
   dictionary
3. a valid `acc_token` in that `session` dictionary

These checks are required to create "sub-sessions" scoped by `record_id` and
to make sure they are properly initialized if there are any errors or missing
data. Why do do this extra work instead of having a simple `record_id` and/or
`acc_token` stored in the browser's cookies? The problem is that a single user
could be using the same app with multiple browser windows open to different
records at the same time. In that case, a single `record_id` or `acc_token`
cookie would be shared between these browser windows creating the possibly for
many types of serious concurrency errors.


### Checking for a `session` for This `record_id`

The following code checks for a `session` cookie that holds all the
"sub-session" data and that there is exists a "sub-session" scoped to the
given `record_id`. If either one is missing a flag `reauth_required_p` is set:

    sessions = flask.session.get('sessions', {})
    if not sessions:
        # no sessions object, create a fresh one
        flask.session['sessions'] = {}
        reauth_required_p = True

    session = sessions.get(record_id, {})
    if not session:
        # no session for this record_id in the sessions object, create one
        sessions[record_id] = {}
        flask.session['sessions'] = sessions
        reauth_required_p = True


### Initialize the SMARTClient

At this point we initialize the client with the line:

    client = _init_smart_client(record_id)

`_init_smart_client()`, simply wraps the call initializing the SMARTClient in
a `try/expect` block so that any errors thrown by the client will be logged
and handled appropriately. Note that a valid `record_id` is not needed to
initialize the client (and that is how we got the `launch_url` earlier). This
is to support the use case where you don't know in advance the record you want
to access and you want the user to be presented with a UI for selecting a
record.


### Check the `acc_token` is Valid

Since we have a "sub-session" for this `record_id`, the next step is to check
that we have a valid access token:

    acc_token = session.get('acc_token', None)
    if not acc_token:
        # missing acc_token for this session
        reauth_required_p = True
    else:
        client.update_token(acc_token)

        if not _test_acc_token(client):
            reauth_required_p = True

If the `acc_token` exists, we "update" the client with it then test it's
validity with `_test_acc_token()`. If that function returned `True`, we know
we already have a valid access token and no further authentication is
required.


### Requesting the Request Token

If we don't have a valid access token for any reason, we'll need to start the
OAuth dance. To do so, we call the helper function:

        _request_token_for_record(record_id, client)

See step (2) in the [Yahoo OAuth
diagram](http://developer.yahoo.com/oauth/guide/oauth-auth-flow.html).

If there were no errors in fetching the request token from the Container, this
helper function saves the returned token in the Flask `sessions` dictionary
with the `record_id` as the index with the lines:

        req_token = client.fetch_request_token()
        sessions = flask.session['sessions']
        sessions[record_id] = {'req_token': req_token, 'acc_token': None}
        flask.session['sessions'] = sessions

The `record_id` being used in the current OAuth process is also stored in it's
own encrypted cookie as a convenience for the next step:

        flask.session['auth_in_progress_record_id'] = record_id


### User Authorization for Access

The next step in the OAuth dance is to have the user signal to the container
that they approve this app's request for access. This corresponds to step (3)
in the diagram. How does the user approve this request for access? Control is
returned to the `index` function and the app the redirects the user's browser
to the container's "access authorization page" defined in the SMARTClient:

     flask.redirect(smart.auth_redirect_url)


### Exchange the Request Token for the Access Token

Once the user authorizes the app's request with the container, the container
will redirect the users' browser to the `oauth_callback` URL ('/authorized' by
convention) defined in the manifest installed within the container. The
container then passes a temporary token, the `oauth_verifer`, as a HTTP
parameter to that callback URL.

The app's handler for this URL must then "exchange" the `request_token` and
the `oauth_verifer` with the container to receive the final `access_token`.
Once the `access_token` is received, the OAuth dance is complete and the app
can now access protected data until the access token expires.

After a couple lines checking that we have the correct tokens, the code makes
a call to the `_exchange_token()` helper function passing in the
`oauth_verifer` sent in the HTTP request arguments:

    # now use the verifier to get the access token
    _exchange_token(record_id,
                    req_token,
                    flask.request.args.get('oauth_verifier'))

Inside the helper function, this call performs the verifier for access token
exchange:

    acc_token = client.exchange_token(verifier)

If that proceeded without error, the access token is then saved in the
`record_id` indexed sub-session, and control returns to the `authorize()`
function which then redirects the user's browser back to `/index`. Now with a
fresh, valid `acc_token` mapped to `record_id` in the session dictionary, the
checks in `/index` will pass, and we can now access the data:

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

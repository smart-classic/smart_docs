---
layout: guide
title: SMART - REST App Tutorial
---

# SMART REST App Tutorial

For many apps you may want to build, the [SMART Connect JavaScript
library](/guide/tutorials/smart_connect.html) will be the only interface you
will need to get the data you require from a SMART container. But if your app
has a backend that needs access to the data as well, you will need to use the
SMART REST API. This tutorial will show you how to setup and use that type of
"server-to-server" data flow.


## Authentication and Authorization is Required

With SMART Connect, authentication and authorization are handled for you by the
SMART Connect library and the SMART Container. Specifically, the JS API call
notified the outer frame (supplied by the SMART Container) of the data request,
and the outer frame already knows the identity of the logged in user and what
medical record that user was currently accessing. Authentication and
authorization of that request happened inside the user's browser without any
effort required of you, the app writer.

Now consider a case where you want the backend of your app to obtain data
directly from the SMART Container. In this case, the SMART Container doesn't
know in advance who is making the call and what data they are authorized to
access. The calls the backend of your app makes must contain information that
proves to the Container that they come from a trusted and pre-authenticated
source.


## Choosing the Right Tools

Since you can write a SMART REST app in many languages and frameworks, you have
great flexibility in choosing the tools you work with. Generally you'll want to
look for a language with existing [OAuth][] libraries to handle the details of
signing requests to the SMART container.

We'll illustrate the highlights of the REST API with a simple Python-based SMART
app called (unimaginatively) [smart_rest_minimal][]. This app is written using
the excellent [Flask][] web microframework. This isn't a tutorial on Flask, but
to get started all you'll need to understand is that Flask provides a simple
mechanism to map HTTP URLs to Python functions.

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


## OAuth Authentication Flow

[Here](http://developer.yahoo.com/oauth/guide/oauth-auth-flow.html) is a diagram
of the OAuth 1.0 flow for visual learners.  SMART REST apps _must_ perform the
standard OAuth 1.0a dance including providing authorization callback URLs.

### Initializing the SMARTClient

First, initialize the SMARTClient with the URL of the SMART container you are
attempting to access (the `api_base`) and your app's `consumer_key` and
`consumer_secret` which you registered with the container previously so the
container can authenticate your app's requests. This may be on you app's users
first hit of your app's `index` page. You may or may not have a patient's
`record_id` at this point.


### Getting the `record_id`

If you don't have a `record_id`, you will be able to redirect to the container's
record selection page (the `smart.launch_url`) which will redirect back to your
app's `index` page with the user selected `record_id` in the URL parameters for
you to read.


### Requesting the Request Token

The next step in the OAuth dance is for your app to request the request_token to
allow access to a specific patient record. This is done simply by initializing
the SMARTClient with the `api_base` and desired `record_id`. Assuming your
initialized SMARTClient is stored in a variable named `smart`:


    smart.fetch_request_token()


### Authorizing the request

If this call was successful, the next step in the dance is to have
the user signal to the container that they approve this request for
access. This is done by having your app redirect the user's browser
to the container's "access authorization page":

     flask.redirect(smart.auth_redirect_url)


### Exchange the Request Token for the Access Token

Once the user authorizes your app's request with the container, the
container will redirect the users' browser to the `oauth_callback` URL
(typically `/authorized`) that you defined in the manifest that you
installed with the container passing an `oauth_verifer` as a HTTP
parameter. Your app's handler for this URL should then "exchange" the
`request_token` and the `oauth_verifer` with the container to receive
the `access_token` which your app will use to make requests for
protected data from the container.

    acc_token = smart.exchange_token(verifier)

### Accessing Protected Data With the Access Token

A few final steps are required before accessing data: your app will need
to store the access token in a web session (or other means) so it can be
reused across multiple requests. And the smart client's internal token
should be "updated" e.g.


    flask.session['acc_token'] = acc_token
    smart.update_token(acc_token)


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

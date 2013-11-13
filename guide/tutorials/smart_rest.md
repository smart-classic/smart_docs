---
layout: guide
title: SMART - REST App Tutorial
---

# SMART REST App Tutorial
(TODO: currently from old documentation site)

# Server to Server Authentication

When your app was making JavaScript API calls, authentication and authorization
were entirely transparent to you, the app builder, because the SMART Container
was able to take care of it all: the JavaScript API call simply notified the
outer frame of the data request, and the outer frame knows who the logged-in
user is and what medical record they're currently considering.

Now, we consider the case where you want the backend of your app to obtain data
directly from the SMART Container, e.g. the SMART Reference EMR, using the REST
API. In that case, the SMART Container doesn't know a-priori who is making the
call and whether they're authorized to do so. We need to authenticate the call
somehow, and you, the app builder, need to know how to ensure that your calls
are properly authenticated.


# Choosing the Right Tools

Since you can write a SMART REST app in any language using any toolkit,
you have a lot of flexibility. In general, you'll want to look for a
language with existing OAuth libraries to handle the details of signing
requests to the SMART container. Here we'll illustrate the highlights
with a simple Python-based SMART REST demo app called unimaginatively
called [smart_rest_minimal][].  This app is written using the [Flask][]
web microframework. This won't be a tutorial on Flask, but to get
started all you'll need to understand is that Flask provides a simple
mechanism to map HTTP URLs to Python functions.

[smart_rest_minimal]: https://github.com/chb/smart_rest_minimal
[flask]: http://flask.pocoo.org/


# Getting to know OAuth

To authenticate your apps' calls to the SMART Container, SMART uses
[OAuth][], an open standard for access delegation.

[oauth]: http://tools.ietf.org/html/rfc5849


OAuth bundles two important features:

1. a way to label and sign HTTP requests using an identifier token and a
secret string

2. a dance involving the user's browser, the data server,
and the server that wishes to consume the data, which, when the user
approves the exchange, provides the data consumer with the token and
secret needed to perform the authenticated API calls as per (1).

SMART employs (1) and, as of SMART v0.6, (2) the full OAuth
authentication "dance".


# Change Your App's OAuth Consumer Secret in Production (Important!)

Each SMART container your app runs against must first "install" your app
by inserting your app's manifest into it's database. This data includes
your app's OAuth `consumer-secret` which is the shared secret between
your app and the container that __ALL SECURITY__ of your app's
communication with the server relies on and is a basic requirement of
OAuth-signed REST API calls.

<div id='consumer_secret_warning' class='red_box'>
  If this secret is revealed to or guessed by a 3rd party, the security of
  your app and the container has been breached! Using the default secret
  ("smartapp-secret") while in development is acceptable, but:
  <br />
  <br />
  <strong>
    <em>
      YOU MUST CHANGE THE <code>consumer-secret</code> IN PRODUCTION!
    </em>
  </strong>
</div>

This secret is provisioned when your app is loaded into the smart
container with the following command:

    $ manage.py load_app <manifest-location> <secret>


# OAuth

SMART REST apps now perform the standard OAuth 1.0a dance including
providing authorization callback URLs instead of the previous
"simplified" dance. This allows developers to use more standard
libraries and methods write native apps (including mobile apps).

Here is a diagram of the OAuth 1.0 flow for you visual learners:
<http://developer.yahoo.com/oauth/guide/oauth-auth-flow.html>


# Authentication Flow

## Initializing the SMARTClient

First, initialize the SMARTClient with the URL of the SMART container
you are attempting to access (the `api_base`) and your app's
`consumer_key` and `consumer_secret` which you registered with the
container previously so the container can authenticate your app's
requests. This may be on you app's users first hit of your app's `index`
page. You may or may not have a patient's `record_id` at this point.


## Getting the `record_id`

If you don't have a `record_id`, you will be able to redirect to the
container's record selection page (the `smart.launch_url`) which will
redirect back to your app's `index` page with the user selected
`record_id` in the URL parameters for you to read.


## Requesting the Request Token

The next step in the OAuth dance is for your app to request the
request_token to allow access to a specific patient record. This is done
simply by initializing the SMARTClient with the `api_base` and desired
`record_id`. Assuming your initialized SMARTClient is stored in a
variable named `smart`:


    smart.fetch_request_token()


## Authorizing the request

If this call was successful, the next step in the dance is to have
the user signal to the container that they approve this request for
access. This is done by having your app redirect the user's browser
to the container's "access authorization page":

     flask.redirect(smart.auth_redirect_url)


## Exchange the Request Token for the Access Token

Once the user authorizes your app's request with the container, the
container will redirect the users' browser to the `oauth_callback` URL
(typically `/authorized`) that you defined in the manifest that you
installed with the container passing an `oauth_verifer` as a HTTP
parameter. Your app's handler for this URL should then "exchange" the
`request_token` and the `oauth_verifer` with the container to receive
the `access_token` which your app will use to make requests for
protected data from the container.

    acc_token = smart.exchange_token(verifier)

## Accessing Protected Data With the acc_token

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

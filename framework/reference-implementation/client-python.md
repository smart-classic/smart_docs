---
layout: default
title: SMART Python Client
---

<div class='simple_box'>
  <p>
    This document describes the SMART Python Library, which you can use from a
    Python application to make authenticated REST calls into a SMART container
    and perform the OAuth authorization dance.
  </p>
  <p>
    You will want to read the
    <a href='/howto/build_a_rest_app/'>SMART REST HOWTO</a> to understand when
    you might want to use this library.
  </p>
    {% include githublink %}
</div>


## Setting Up Your Environment

To use the SMART Python client library, you need, of course, to be
running a Python app. The most common use case for using this library is
implementing the web backend for your SMART App, using a toolkit such as
[Flask](http://flask.pocoo.org/) or [Django](http://djangoproject.com/).


## Get the Code

The SMART client library is on Github:

  $ git clone https://github.com/chb/smart_client_python.git

You will notice `generate_api.py` and `generate_readme.py` inside the newly formed
directory `smart_client_python`. You do NOT need to run these. The API is
pre-generated from the OWL specification. Unless you plan on changing the OWL
specification (and it's very likely you don't want to do that), you won't need
to run these utilities.

Also, you'll need `rdflib`, a Pythonic RDF library:

{% highlight sh %}
  $ sudo apt-get install python-pyparsing
  $ sudo easy_install -U "rdflib>=3.0.0"
  $ sudo easy_install rdfextras
{% endhighlight %}


## Set your Python Path

You need to make sure that `smart_client_python` (which you can rename
without any complication, e.g. to smart_client) is in your Python path
when you run your application. The easiest way to do this is to
git-clone/copy/symlink the directory into your application path. If
you're using git to manage your repository, you may want to set up
`smart_client_python` as a git submodule (but do this _only_ if you
understand git submodules well.)


## Import the Right Modules

For starters, you'll need the main module:

{% highlight python %}
  from smart_client_python.client import SMARTClient
{% endhighlight  %}


## Using the SMART Client

To make a SMART REST API call, you'll need to instantiate a
`SMARTClient` object, optionally setting its record_id, and choose the
call you want to make.

{% highlight python %}
  client = SMARTClient(APP_ID, API_BASE, CONSUMER_PARAMS_DICT)
{% endhighlight  %}

In this call:

* `APP_ID`: Your app's id

* `API_BASE`: the URL base to which SMART API REST calls are made, e.g.:

{% highlight python %}
    API_BASE = 'http://sandbox-api.smartplatforms.org'
{% endhighlight %}

* `CONSUMER_PARAMS_DICT`: a Python dictionary containing your app's OAuth
  consumer credentials:

{% highlight python %}
  `CONSUMER_PARAMS_DICT` = {
      'consumer_key': 'my-app@apps.smartplatforms.org',
      'consumer_secret' : 'smartapp-secret'
  }
{% endhighlight %}

Once instantiated, a SMART client object can be used for as many API
calls as needed. If you need to use different credentials, in particular
to access resources of a different record, you should instantiate a new
`SMARTClient`.


### SMART Client Record Context

The `SMARTClient` object contains a little bit of additional context: the
`record_id`. This can be set like any normal Python attribute:

{% highlight python %}
  client.record_id = '157'
{% endhighlight  %}

If you do not set up this context on initialization by passing it in as
an item of the CONSUMER_PARAMS_DICT, you will have to provide the `record_id`
parameter on every API call.


### Where do I Get the Tokens?

The consumer key and secret are defined once for your app when it is set
up within the SMART Container. If you're developing against the SMART
Reference EMR Sandbox, you'll want to use:

{% highlight python %}
{
    'consumer_key': 'my-app@apps.smartplatforms.org',
    'consumer_secret': 'smartapp-secret'
}
{% endhighlight  %}

See the warning about setting a strong `consumer_secret`
[here](/howto/build_a_rest_app)


## Call Authorization

Before the SMART container accepts any calls, you need to have been authorized
and issued an access token. You receive an access token through a three-legged
OAuth dance performed like this:

1. Request a token: `client.fetch_request_token()`
2. Have the user visit `client.auth_redirect_url` in his Browser
3. When the user authorizes the app he will be redirected to the `oauth_callback`
   URL specified in your app's manifest. Extract the `oauth_verifier` from the
   callback URL and make the client exchange the request token for an access
   token:
   `client.exchange_token(oauth_verifier)`

If these steps complete successfully the client now has an access token and you
can start making calls. Here is a minimal working example on how to receive an
access token; note that you will receive the `record_id` passed to your `index`
URL when the user starts your app, for simplicity reasons we assume a record id
here:

{% highlight python %}
  smart = SMARTClient(API_BASE, CONSUMER_PARAMS_DICT)

  # request a token for a specific record id
  smart.record_id = '1288992'
  smart.fetch_request_token()
  print 'Now visit:  %s' % smart.auth_redirect_url
  oauth_verifier = raw_input('Enter the oauth_verifier: ')

  # exchange the token
  smart.exchange_token(oauth_verifier)
{% endhighlight %}


## Making the Call

To get, say, the list of medications on a record, you can simply make the
following call:

{% highlight python %}
  medications = client.get_medications()
{% endhighlight  %}

Notice that the method signature follows the definitions on our [REST
API Page](/reference/rest_api).


## Working with the Results

The results of a SMART API call using the client library is an `SMARTResponse`
object containing the RDF graph. For more on RDF graphs, please read our
[Quick Intro to RDF and SPARQL][rdf intro]. At a high-level, the result is a
dataset that can be manipulated and queried in a very flexible manner. You can
use `rdflib` to do just that:

For example, if we want the list of medication names

{% highlight python %}
  query = """
           PREFIX dcterms:<http://purl.org/dc/terms/>
           PREFIX sp:<http://smartplatforms.org/terms#>
           PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
           SELECT ?drugname
           WHERE {
             ?med rdf:type sp:Medication .
             ?med sp:drugName ?drugname_code.
             ?drugname_code dcterms:title ?drugname.
           }
           """
  med_names = medications.graph.query(query)
{% endhighlight  %}


## API Reference

All REST API calls can be used by the SMART client library simply by mapping the
REST URL signature to a Python method signature as described above for the
medications use case. Check out our [API][]. You can also use command

{% highlight sh %}
  $ python generate_readme.py
{% endhighlight  %}

to automatically generate the available methods in the client library.

If you don't want to run that code yourself, check out this library' README on
[github](http://github.com/chb/smart_client_python).

---
layout: container
title: SMART - Container Manifests
---

<div class='simple_box'>
  Note: This document describes SMART **container** manifests not <a
  href='/framework/manifests/'>SMART **app** manifests</a>.
</div>


### Introduction to Container Manifests

To help apps know the capabilities and other useful information about your
container, you must provide a JSON manifest file at
<http://mysmartcontainer/manifest>.


### An Example Container Manifest

This is the complete manifest file of the SMART Reference container accessible
at <http://sandbox-api-v10.smartplatforms.org/manifest>. We'll describe each
section of the file below. 

{% highlight javascript %}
{
    "name": "SMART v1.0 Sandbox", 
    "description": "Public sandbox to demonstrate the SMART API", 
    "admin": "e-mail-support-address@host.com", 
    "smart_version": "1.0",

    "api_base": "http://sandbox-api-v10.smartplatforms.org", 
    "launch_urls": {
        "app_launch": "http://sandbox-v10.smartplatforms.org/apps/{{app_id}}/launch", 
        "authorize_token": "http://sandbox-v10.smartplatforms.org/oauth/authorize", 
        "exchange_token": "http://sandbox-api-v10.smartplatforms.org/oauth/access_token", 
        "request_token": "http://sandbox-api-v10.smartplatforms.org/oauth/request_token"
    }, 

    "capabilities": {
        "http://smartplatforms.org/terms#Allergy": {
            "methods": [
                "GET"
            ]
        }, 
        "http://smartplatforms.org/terms#AppManifest": {
            "methods": [
                "GET"
            ]
        }, 

        // many more here ...
    } 
}
{% endhighlight  %}


### Basic Container Identification

{% highlight javascript %}
    "name": "SMART v1.0 Sandbox", 
    "description": "Public sandbox to demonstrate the SMART API", 
    "admin": "e-mail-support-address@host.com", 
    "smart_version": "1.0",
{% endhighlight  %}

The manifest contains some basic information about your container.

- `name` - the pretty name of your container
- `description` - a longer description of your container
- `admin` - the email address of the container administrator
- `smart_version` - the version of the SMART API and data models your
  container supports


### OAuth URLs

{% highlight javascript %}
    "api_base": "http://sandbox-api-v10.smartplatforms.org",
    "launch_urls": {
        "app_launch": "http://sandbox-v10.smartplatforms.org/apps/{{app_id}}/launch",
        "request_token": "http://sandbox-api-v10.smartplatforms.org/oauth/request_token",
        "authorize_token": "http://sandbox-v10.smartplatforms.org/oauth/authorize"
        "exchange_token": "http://sandbox-api-v10.smartplatforms.org/oauth/access_token",
    }, 
{% endhighlight  %}

Apps that use the [SMART REST API](/guide/tutorials/smart_rest.html) need to
know the URLs your container provides for the various steps of the OAuth dance:

- `api_base`: the base URL of your container. REST paths are relative to this
  URL, so apps need to know the base URL to build request URLs.
- `app_launch`: this URL can be called to have a container launch a specific
  app. The app to launch is specified by the `{{app_id}}` placeholder and the
  container will display the app's launch page, potentially after prompting
  to log in. If the <a href='/framework/manifests/'>app's manifest</a> specifies
  the `standalone` flag, the container should open the app's index page in a
  new window or tab, otherwise the app can be launched inside the container's
  iframe.
- `request_token`: to initiate the OAuth dance, the app will request a request
  token from this URL.
- `authorize_token`: after the app received a request token, the user must
  authorize the token. For this step the app must load the authorize URL in a
  browser view where the user can login, if not already done so, and authorize
  the token manually, if not previously done so. The container will return the
  oauth_verifier to the app.
- `exchange_token`: finally, the request token and the oauth_verifier obtained
  at the previous URLs can be exchanged for an access token at this URL. The
  container returns an access token that the app can then use to make requests.


### Capabilities

{% highlight javascript %}
    "capabilities": {
        "http://smartplatforms.org/terms#Allergy": {
            "methods": [
                "GET"
            ]
        }, 
        "http://smartplatforms.org/terms#AppManifest": {
            "methods": [
                "GET"
            ]
        }, 
        "http://smartplatforms.org/terms#ClinicalNote": {
            "methods": [
                "GET", 
                "POST"
            ]
        }, 
        "http://smartplatforms.org/terms#ContainerManifest": {
            "methods": [
                "GET"
            ]
        }, 
        "http://smartplatforms.org/terms#Demographics": {
            "methods": [
                "GET"
            ]
        }, 

        ...

        "http://smartplatforms.org/terms#ScratchpadData": {
            "methods": [
                "GET", 
                "PUT", 
                "DELETE"
            ]
        }, 

        ...

        "http://smartplatforms.org/terms#UserPreferences": {
            "methods": [
                "GET", 
                "PUT", 
                "DELETE"
            ]
        }
    } 
{% endhighlight  %}

The capabilities section lists all the [SMART API calls](/framework/api/) that
your container supports. Most of the API calls respond only to HTTP GET method
requests due to the fact that the SMART API is mostly read-only, however there
are a few exceptions:

- [ClinicalNote](/framework/api/#record_clinical_note)
- [ScratchpadData](/framework/api/#record_scratchpad_data)
- [UserPreferences](/framework/api/#user_user_preferences)


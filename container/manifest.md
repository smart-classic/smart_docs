---
layout: container
title: SMART - Container Manifests
---

<div class='simple_box'>
  Note: This document describes SMART container manifests not SMART app
  manifests! For information on SMART app manifests see <a
  href='/framework/manifests/'>here</a>.
</div>


### Introduction to Container Manifests

To help apps know the capabilities and other useful information about your
container, you should provide a JSON manifest file at
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
        "authorize_token": "http://sandbox-v10.smartplatforms.org/oauth/authorize", 
        "exchange_token": "http://sandbox-api-v10.smartplatforms.org/oauth/access_token", 
        "request_token": "http://sandbox-api-v10.smartplatforms.org/oauth/request_token"
    }, 
{% endhighlight  %}

Apps that use the [SMART REST API](/guide/tutorials/smart_rest.html) need to
know the URLs your container provides for the various steps of the OAuth
"dance". The most important one is the `api_base`.

TODO: describe use of `launch_urls`.


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


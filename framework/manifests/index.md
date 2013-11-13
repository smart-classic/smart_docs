---
layout: framework
title: SMART - Using Manifest Files
---

## Introducing SMART Manifests

Each SMART app should provide a JSON manifest to declare itself to the
container. This manifest defines the app's name, ID, a description, and its
application mode.

If you're building a straightforward SMART Connect App, here's a template you
can use for your manifest file. Just replace the ALL-CAPS placeholders with
your own values.

{% highlight javascript %}
  {
    "name" : "YOUR APP NAME",
    "description" : "BRIEF DESCRIPTION FOR IN-LINE DISPLAY",
    "author" : "YOUR NAME",
    "id" : "CHOOSE-AN-ID@apps.smartplatforms.org",
    "version" : "YOUR.VERSION.NUMBER",

    "mode" : "ui",
    "standalone": false,
    "scope": "record",

    "index" : "http://PATH/TO/YOUR/index.html",
    "icon" : "http://PATH/TO/YOUR/icon.png"
  }
{% endhighlight  %}


## Application Modes

SMART Applications can run in one of two modes:

* UI Apps mode (`ui`): These apps interact with the user in the context of
  the SMART container. Several of the sample apps fall in this category the
  Med List, Problems List, and Got Statins apps. These are SMART's "normal"
  apps.

* Frame UI Apps mode (`frame_ui`): These apps can launch and layout multiple
  apps side-by-side. Apps in this category include: i2b2 EMR View, as well as
  our Frame UI Example app in our sample apps repository.


## Standalone Apps

If the app can run in its own browser window (or is a non-browser app such as a
native iOS or Android app) set the `standalone` flag to `true`. It is false by
default and may be omitted from the manifest.


## Sample Manifest Files

A UI App provides an index file and an icon. Optionally, the manifest file can
declare the SMART container version and the API calls that the app needs. For
example, this is the Meds List app manifest:

{% highlight javascript %}
  {
    "name":        "Med List",
    "description": "Display medications in a table or timeline view",
    "author":      "Josh Mandel, Children's Hospital Boston",
    "id":          "med-list@apps.smartplatforms.org",
    "version":     ".1a",

    "mode" : "ui",
    "scope": "record",

    "icon" : "http://localhost:8001/framework/med_list/icon.png",
    "index": "http://localhost:8001/framework/med_list/index.html",

    "smart_version": "0.6",

    "requires" : {
      "http://smartplatforms.org/terms#Medications": {
        "methods": ["GET"]
      },
      "http://smartplatforms.org/terms#Demographics": {
        "methods": ["GET"]
      }
    }
  }
{% endhighlight  %}


## Add `oauth_callback` for SMART REST Apps

If you are writing a manifest for a SMART REST app the `oauth_callback`
parameter is required. Read the full details at the [REST
tutorial](/guide/tutorials/smart_rest.html)


## Validating Your Manifest

The API Verifier app has a facility for validating SMART manifests. You can
either launch the app on the sandbox container or in standalone mode from this
URL <http://apiverifier.smartplatforms.org/smartapp/index.html>. Click on the
"Manifest" tab, copy in your manifest's text, then click the "Validate" button
to validate.


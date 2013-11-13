---
layout: guide
title: SMART - Frame App Tutorial
---

# SMART Frame App Tutorial
(TODO: currently from old documentation site)

# What is a Frame UI App?

<a href="{{BASE_PATH}}/images/frame_ui_screenshot.png" target="_blank">
    <img src="{{BASE_PATH}}/images/frame_ui_screenshot.png"
    style="width: 100%; display: block; margin: 20px auto;">
</a>


SMART v0.4 allows developers to build a kind of meta-app, or "Frame UI App" that
can lay out multiple traditional UI Apps at the same time. For example, let's
say you'd like to display a medication list app right alongside a medication
adherence app. You can accomplish this by writing a Frame UI app that lays them
both out on the screen simultaneously.

For example, the Frame UI app in this screenshot allows a user to select two
apps to display side-by-side:


## What can Frame UI Apps do?

* Present an HTML5 user-interface in-browser
* Obtain a list of apps that are installed in this container
* Launch multiple other UI Apps, incorporating them, for example, in a tiled grid


## Declaring a Frame UI App

Because Frame UI apps have extra capabilities such as listing and launching
other apps, they need extra permissions from the container. To communicate this
fact, a Frame UI app include the following line in its SMART Manifest:

{% highlight javascript %}
  "mode" : "frame_ui"
{% endhighlight  %}


## Building blocks

Frame UI apps occupy a unique place in the SMART architecture, since they're
_apps_ that also have some capabilities of _containers_. In other words,
they _are_ apps and they can also _run_ apps. To make this work, Frame UI
apps need to include three javascript libraries:

* `smart-api-client.js` to act as an app
* `smart-api-container.js` to launch other apps
* `smart-frame-ui.js` glue between the two libraries above


## Example Frame UI App

Let's work through an example of a simple Frame UI app that can display three
SMART apps a time, and allows the user to select these apps. First off, let's
see what apps are available to launch and load them into a "Carousel" of choices
to display:


### Displaying a "carousel" of available apps:

{% highlight javascript %}
  SMART.get_manifests(function(response) {
             manifests = response.json;
             carousel.html("");

             // Populate a carousel element for each available app.
             jQuery.each(manifests, function(i,m) {
               var app = jQuery("<img src='"+m.icon+"' title='"+m.name+ ": " + m.description + "'>");
               carousel.append(app);
               app.click(function(){
                 SMART_HOST.launch_app(m, SMART.context);
               });
             });
       });
{% endhighlight  %}

This code fetches a list of manifests from the container `SMART.get_manifests`,
loops through them, and displays an icon for each app available. It then
attaches a click handler to each icon: when clicked, we call
SMART_HOST.launch_app to initiate the launch of this new app. We pass in the
app's manifests `m` and our current context `SMART.context`, which specifies the
user and record.


### Handling an app launch:

When a user clicks on an app icon and SMART_HOST.launch_app is called, the
SMART libraries take care of most details of the app launch process. But the
SMART libraries expect a little bit of "help" (in the form of a helper
function) to determine which IFRAME element to use in positioning the
newly-launched app. Since our Frame UI app will perform a pretty simple layout,
this doesn't take much. We'll assume that three IFRAMES are available on the
screen at all times, and we'll just populate them in order, looping back to the
beginning when they're all full.

{% highlight javascript %}
     var current_iframe = 0;
     var iframes_available = 3;

     SMART_HOST.get_iframe = function (app_instance, callback){
       callback($("iframe")[current_iframe % iframes_available]);
       current_iframe++;
     };
{% endhighlight  %}


## See it live

You can view the example app at:
[http://sandbox-dev.smartplatforms.org](http://sandbox-dev.smartplatforms.org)
(just create an account and add the "Frame UI Example" app.)

You can see the code at:
[https://github.com/chb/smart_sample_apps/tree/dev/static/framework/frame_ui_example](https://github.com/chb/smart_sample_apps/tree/dev/static/framework/frame_ui_example) 

---
layout: framework
title: SMART - JavaScripe Client
---

# What is `smart-api-client.js`?

Every SMART UI app includes an `index.html` page that loads the
`smart-api-client.js` Javascript library to provide the app's functionality.
This page describes the functionality that including `smart-api-client.js`
provides.


# Including `smart-api-client.js`

You include this file in every additional page of your app, e.g. via the
HTML `<script>` tag:

{% highlight html %}
 <script src="http://sample-apps.smartplatforms.org/framework/smart/scripts/smart-api-client.js"></script>
{% endhighlight %}

Once this script loads, your app will have access to a javascript variable
called `SMART`, which can be used to interact with the SMART container via the
calls described below.


# Interacting With the SMART Container via Javascript

Inside your `index.html` file, you'll need to be sure the SMART library has
finished loading before you can use it. Just put your code inside a call to
`SMART.ready()` as shown below. Then you're all set to try out the features
below!

The Javascript SMART object contains some helpful context describing the
current SMART container user and patient record:

* `SMART.user` contains {id, full_name}
* `SMART.record` contains  {id, full_name}

So, for example, to announce the patient's name, you could:

{% highlight javascript %}
  alert("The current patient is: " + SMART.record.full_name);
{% endhighlight %}

If you're looking to make some SMART REST calls, you may be interested in using
REST authentication tokens, which you can access with:

* `SMART.credentials.rest_token`
* `SMART.credentials.rest_sec`

Or you can get the complete SMART OAuth header for your app with:

* `SMART.credentials.oauth_header`


# Calling Another App: A Hint of Inter-Application Workflow

SMART 0.5 introduces a primitive to support in-browser inter-application
workflow: one app can `call` another, passing along some launch data and
receiving a response when the called app finishes.  The basic flow looks like
this:

## In the Call_ing_ App

To start, you'll need a copy of the manifest for the app you want to call.
Then you call it with `SMART.call_app`, passing along the manifest and any
launch data you'd like the called app to receive:

{% highlight javascript %}
 SMART.get_manifest({
   descriptor:"app-to-call@apps.smartplatforms.org"
  }, function(p) {
   var m = p.json;
   SMART.call_app(m, {/*launch data*/}, function(result) {
     console.log("Returned from call:" );
     console.log(result);
   });
 });
{% endhighlight %}

## In the Call_ed_ App

The called app launches just like any SMART app.  If your apps expects any
custom data at launch time, these should be available in: `SMART.ready_data`

When you're app is thruogh, you can call `SMART.complete`, passing in
any return data to be provided for the calling app.

{% highlight javascript %}
   SMART.complete({ 
     /* return data...*/
   });
{% endhighlight %}


# Notifications To and From the SMART Container

## Subscribe to Notifications From the SMART Container

A container will notify an app when important events occur. Today the SMART API
defines three Container-to-app notifications that your app can subscribe to:

* `backgrounded`: the app has been hidden from view
* `foregrounded`: the app has been restored to view
* `destroyed`: the app is being shut down

Your app can use the `on` directive to take action when a notification arrives:

{% highlight javascript %}
  SMART.on("foregrounded", function() {
    refreshAllData();
    alert("Thanks for looking again!");
  });
{% endhighlight  %}

## Send Notifications To the SMART Container

Your app can also send notifications to the container. Today the SMART API
defines only a single App-to-Container notification, which allows an app to
request additional screen real estate when there's something big to display:

{% highlight javascript %}
  SMART.notify_host("request_fullscreen");
{% endhighlight  %}

Please keep in mind that these app->container and container-->app notifications
are "fire and forget"; they don't provide a callback mechanism.


# Making API Calls

You can also use the SMART javascript object to make any [API][] by calling its
`api_call` method, which takes two parameters:

1. a dictionary of:
  * `method`: the HTTP method as string ('GET', 'POST', 'PUT', or 'DELETE')
  * `url`: the URL to post to, relative to the SMART container's API base
  * `contentType`: the contentType as string (default: 'application/x-www-form-urlencoded')
  * `data`
    * as string (for data other than x-www-form-urlencoded data) OR
    * as a dictionary (for x-www-form-urlencoded data)
2. a callback function of
  * `contentType`: a string set according to the response header
  * `data`: a string representation of data

For example, we could retrieve all medications for the in-context record by
calling:

{% highlight javascript %}
  SMART.api_call(
    {
      method: 'GET',
      url: "/records/" + SMART.record.id + "/medications/",
      data: {}
    },
    function(response) { alert('data received: ' + response.body); });
{% endhighlight  %}


# Convenience Wrappers Around Common API Calls

But you shouldn't need to use the raw `.api_call` method very often,
because the SMART javascript object also provides convenience wrappers
around common API calls. The functions below all take a callback
function of one argument: the RDF graph that holds the response data,
parsed from raw RDF/XML via
[rdfquery](http://code.google.com/p/rdfquery/).

# Understanding Error Handling in SMART Connect

The API call methods in SMART Connect support jQuery-style callback
handlers. You can register two separate callbacks:  one for successful
API calls (required) and an optional handler that will be triggered in
the event of an error.  The basic pattern looks like this:

    SMART.get_medications().success(callback_ok).error(callback_err);

Where `callback_ok` and `callback_err` are your callback functions.
`callback_ok` will be called with a SMART response object as argument
when the call succeeds. `callback_err` will be called with a SMART error
object in the event of a failure.

The SMART error object has the following properties:

1. `status`: The status code of the error
2. `message`: An object containing details about the error
   1. `contentType`: The MIME type of the error message descriptor
   2. `data`: The error message description

Putting all of this together we get the following code example:

{% highlight javascript %}
    SMART.get_problems()
         .success(function(problems) {
           var graph = problems.graph;
            // processing here?
         })
         .error(function(e) {
           var status = e.status,
               message = e.message;
           // display error
         });
{% endhighlight  %}


[API]: /reference/rest_api

# A Quick Example

{% highlight javascript %}
  SMART.ready(function() {
    alert("Hello, " + SMART.user.full_name);
  });
{% endhighlight  %}


---
---
---

# API Reference


<!-- GENERATED DOCS INSERTED BELOW THIS LINE - DON'T EDIT OR REMOVE ME! -->



## `delete_scratchpad_data`

- method: DELETE
- path: `/records/{record_id}/apps/{smart_app_id}/scratchpad`


## `delete_user_preferences`

- method: DELETE
- path: `/users/{user_id}/apps/{smart_app_id}/preferences`


## `get_allergies`

- method: GET
- path: `/records/{record_id}/allergies/`
  - optional query parameters (with defaults):
      <br><pre><code>
        "date_from_excluding": null, 
        "date_from": null, 
        "date_to": null, 
        "limit": null, 
        "date_to_excluding": null, 
        "date_from_including": null, 
        "date_to_including": null</code></pre>


## `get_allergy`

- method: GET
- path: `/records/{record_id}/allergies/{allergy_id}`


## `get_app_manifest`

- method: GET
- path: `/apps/{descriptor}/manifest`


## `get_app_manifests`

- method: GET
- path: `/apps/manifests/`
  - optional query parameters (with defaults):
      <br><pre><code>
        "limit": null</code></pre>


## `get_clinical_note`

- method: GET
- path: `/records/{record_id}/clinical_notes/{clinical_note_id}`


## `get_clinical_notes`

- method: GET
- path: `/records/{record_id}/clinical_notes/`
  - optional query parameters (with defaults):
      <br><pre><code>
        "date_to": null, 
        "date_from_excluding": null, 
        "date_from": null, 
        "date_to_excluding": null, 
        "date_from_including": null, 
        "date_to_including": null, 
        "limit": null</code></pre>


## `get_container_manifest`

- method: GET
- path: `/manifest`


## `get_demographics`

- method: GET
- path: `/records/{record_id}/demographics`


## `get_document`

- method: GET
- path: `/records/{record_id}/documents/{document_id}`
  - optional query parameters (with defaults):
      <br><pre><code>
        "format": null</code></pre>


## `get_documents`

- method: GET
- path: `/records/{record_id}/documents/`
  - optional query parameters (with defaults):
      <br><pre><code>
        "limit": null, 
        "format": null</code></pre>


## `get_encounter`

- method: GET
- path: `/records/{record_id}/encounters/{encounter_id}`


## `get_encounters`

- method: GET
- path: `/records/{record_id}/encounters/`
  - optional query parameters (with defaults):
      <br><pre><code>
        "limit": null</code></pre>


## `get_family_history_observation`

- method: GET
- path: `/records/{record_id}/family_history/{family_history_id}`


## `get_family_history_observations`

- method: GET
- path: `/records/{record_id}/family_history/`
  - optional query parameters (with defaults):
      <br><pre><code>
        "limit": null</code></pre>


## `get_fulfillment`

- method: GET
- path: `/records/{record_id}/fulfillments/{fulfillment_id}`


## `get_fulfillments`

- method: GET
- path: `/records/{record_id}/fulfillments/`
  - optional query parameters (with defaults):
      <br><pre><code>
        "date_from_excluding": null, 
        "date_from": null, 
        "date_to": null, 
        "date_to_including": null, 
        "date_from_including": null, 
        "date_to_excluding": null, 
        "limit": null</code></pre>


## `get_immunization`

- method: GET
- path: `/records/{record_id}/immunizations/{immunization_id}`


## `get_immunizations`

- method: GET
- path: `/records/{record_id}/immunizations/`
  - optional query parameters (with defaults):
      <br><pre><code>
        "date_to": null, 
        "date_from_excluding": null, 
        "date_from": null, 
        "date_to_excluding": null, 
        "date_from_including": null, 
        "date_to_including": null, 
        "limit": null</code></pre>


## `get_lab_panel`

- method: GET
- path: `/records/{record_id}/lab_panels/`


## `get_lab_panels`

- method: GET
- path: `/records/{record_id}/lab_panels/`
  - optional query parameters (with defaults):
      <br><pre><code>
        "limit": null</code></pre>


## `get_lab_result`

- method: GET
- path: `/records/{record_id}/lab_results/{lab_result_id}`


## `get_lab_results`

- method: GET
- path: `/records/{record_id}/lab_results/`
  - optional query parameters (with defaults):
      <br><pre><code>
        "loinc": null, 
        "date_from_excluding": null, 
        "date_from": null, 
        "date_to": null, 
        "limit": null, 
        "date_from_including": null, 
        "date_to_excluding": null, 
        "date_to_including": null</code></pre>


## `get_medication`

- method: GET
- path: `/records/{record_id}/medications/{medication_id}`


## `get_medications`

- method: GET
- path: `/records/{record_id}/medications/`
  - optional query parameters (with defaults):
      <br><pre><code>
        "date_from_excluding": null, 
        "date_from": null, 
        "date_to_excluding": null, 
        "limit": null, 
        "date_from_including": null, 
        "date_to": null, 
        "date_to_including": null, 
        "rxnorm": null</code></pre>


## `get_ontology`

- method: GET
- path: `/ontology`


## `get_photograph`

- method: GET
- path: `/records/{record_id}/photograph`


## `get_problem`

- method: GET
- path: `/records/{record_id}/problems/{problem_id}`


## `get_problems`

- method: GET
- path: `/records/{record_id}/problems/`
  - optional query parameters (with defaults):
      <br><pre><code>
        "date_from_excluding": null, 
        "date_from": null, 
        "date_to_excluding": null, 
        "date_to_including": null, 
        "date_from_including": null, 
        "snomed": null, 
        "date_to": null, 
        "limit": null</code></pre>


## `get_procedure`

- method: GET
- path: `/records/{record_id}/procedures/{procedure_id}`


## `get_procedures`

- method: GET
- path: `/records/{record_id}/procedures/`
  - optional query parameters (with defaults):
      <br><pre><code>
        "date_from_excluding": null, 
        "date_from": null, 
        "date_to": null, 
        "date_from_including": null, 
        "snomed": null, 
        "date_to_including": null, 
        "limit": null, 
        "date_to_excluding": null</code></pre>


## `get_scratchpad_data`

- method: GET
- path: `/records/{record_id}/apps/{smart_app_id}/scratchpad`


## `get_social_history`

- method: GET
- path: `/records/{record_id}/social_history`


## `get_user`

- method: GET
- path: `/users/{user_id}`


## `get_user_preferences`

- method: GET
- path: `/users/{user_id}/apps/{smart_app_id}/preferences`


## `get_vital_sign_set`

- method: GET
- path: `/records/{record_id}/vital_sign_sets/{vital_sign_set_id}`


## `get_vital_sign_sets`

- method: GET
- path: `/records/{record_id}/vital_sign_sets/`
  - optional query parameters (with defaults):
      <br><pre><code>
        "date_from_excluding": null, 
        "date_from": null, 
        "date_to": null, 
        "limit": null, 
        "date_from_including": null, 
        "date_to_excluding": null, 
        "date_to_including": null, 
        "encounter_type": null</code></pre>


## `post_clinical_note`

- method: POST
- path: `/records/{record_id}/clinical_notes/`


## `put_scratchpad_data`

- method: PUT
- path: `/records/{record_id}/apps/{smart_app_id}/scratchpad`


## `put_user_preferences`

- method: PUT
- path: `/users/{user_id}/apps/{smart_app_id}/preferences`


## `search_records`

- method: GET
- path: `/records/search`
  - optional query parameters (with defaults):
      <br><pre><code>
        "family_name": null, 
        "gender": null, 
        "app_id": null, 
        "date_of_birth": null, 
        "limit": null, 
        "given_name": null, 
        "medical_record_number": null</code></pre>


## `search_users`

- method: GET
- path: `/users/search`
  - optional query parameters (with defaults):
      <br><pre><code>
        "family_name": null, 
        "limit": null, 
        "given_name": null</code></pre>


---
layout: default
title: SMART Developers Documentation
---

# SMART Connect Tutorial
(currently from old documentation site)

## Index

The index file, served at
[http://localhost:8000/smartapp/index.html](http://localhost:8000/smartapp/index.html)
is where all the fun happens! Make sure to include the SMART page script:

{% highlight html %}
    <script src="http://sample-apps.smartplatforms.org/framework/smart/scripts/smart-api-client.js"></script>
{% endhighlight  %}

This script serves to connect your HTML page to the SMART JavaScript library.

Once the client-side library has loaded, your index HTML page has access to a
SMART JavaScript object that provides some basic context:

<ul>
  <li>`SMART.user`, which provides the name and ID of the user who
      launched the app, typically the physician logged into the SMART EMR.</li>
  <li>`SMART.record`, which provides the name and ID of the patient whose record is loaded.</li>
</ul>

For a complete reference of the app context, check out the JavaScript Library
reference.

A more complete index file that displays the current patient's name might thus
look like:

{% highlight html %}
    <!DOCTYPE html>
    <html>
     <head>
      <script 
src="http://sample-apps.smartplatforms.org/framework/smart/scripts/smart-api-cli
ent.js"></script>
     </head>
     <body><h1>Hello <span id="name"></span></h1>

     <script>
       SMART.ready(function(){
         document.getElementById('name').innerHTML = SMART.record.full_name;
       });
     </script>
     </body>
    </html>
{% endhighlight  %}


# Using the SMART API

At this point, your SMART app is ready to make API calls to obtain health data.
Remember that your app is instantiated in an IFRAME for the specific purpose of
accessing a single medical record. This means that, from JavaScript, you can
request medical data without specifying patient context, because it's already
determined by the JavaScript context.


## Asynchronous Calls

Let's load the patient's medications using SMART.get_medications(). The most
important thing you need to know about all SMART JavaScript APIs is that they
are asynchronous: you won't get the meds as a result of the
SMART.get_medications() call. Instead, you need to specify callback functions
that will be invoked when the results are ready:

{% highlight javascript %}
    SMART.get_medications().success(function(meds) {
      // do something with those meds
    }).error(function(err) {
      // handle the error
    });
{% endhighlight  %}

Why did we design the API this way? Because, in most cases, the SMART container
will need to make a call to a server to obtain the requested data. That could
take some time, and it would be very unfortunate if your app was forced to block
for a couple of seconds. Instead, your app gets control back from the SMART
library call almost immediately and is free to display some pretty progress bar
or, more substantively, make additional API calls to obtain a few data points in
parallel.


## Data in RDF form

When data becomes available, the SMART framework invokes your callback function,
passing it the resulting medications as a parameter. This result is in the form
of an SMARTResponse object containing the RDF graph. RDF (Resource Description
Framework) is an open and flexible approach to modeling all kinds of data in a
graph structure. If you haven't used RDF, you should read our Quick Introduction
to RDF and SPARQL.

The bottom line is a SMART medication list is an RDF graph that can be easily
navigated and queried. For example, if meds is an RDF graph, then:

{% highlight javascript %}
  meds.graph.where("?medication rdf:type sp:Medication")
{% endhighlight  %}

selects all of "objects" in the graph that have a datatype sp:Medication, where
sp stands for [http://smartplatforms.org/ns#](http://smartplatforms.org/ns#),
the location of the SMART vocabulary.

Of course, we want more than just the raw "objects," we want their properties,
in particular the name of the drug. The following selects the drug names, which
are coded-values, and then the value of those coded values, which are the actual
drug-name strings:

{% highlight javascript %}
    meds.graph
        .where("?medication rdf:type sp:Medication")
        .where("?medication sp:drugName ?drug_name_code")
        .where("?drug_name_code dcterms:title ?drugname");
{% endhighlight  %}

This is effectively a JavaScript query on the RDF graph, and it returns a set of
JavaScript objects with properties we're interested in, in particular drugname.
We can then iterate over the list of returned objects and extract the drugname
property for each one:

{% highlight javascript %}
    var med_names = meds.graph
             .where("?medication rdf:type sp:Medication")
             .where("?medication sp:drugName ?drug_name_code")
             .where("?drug_name_code dcterms:title ?drugname");

         med_names.each(function(i, single_med) {
             // do something with single_med.drugname
           });
{% endhighlight  %}


## The Complete App

So, to display the patient's medications, we set up an HTML list, \<ul>, and we
append to it with the name of each drug in our iteration:

{% highlight html %}
    <!DOCTYPE html>
    <html>
     <head>
      <script src="http://sample-apps.smartplatforms.org/framework/smart/scripts/smart-api-client.js"></script>
     </head>
     <body><h1>Hello <span id="name"></span></h1>

     <ul id="med_list"></ul>
     
     <script>
       SMART.ready(function(){
         document.getElementById('name').innerHTML = SMART.record.full_name;
         SMART.get_medications().success(function(meds) {
           var med_names = meds.graph
             .where("?medication rdf:type sp:Medication")
             .where("?medication sp:drugName ?drug_name_code")
             .where("?drug_name_code dcterms:title ?drugname");

           var med_list = document.getElementById('med_list');
           med_names.each(function(i, single_med) {
             med_list.innerHTML += "<li> " + single_med.drugname + "</li>";
           });
         }).error(function(err) { alert ("An error has occurred"); });
       });
     </script>
     </body>
    </html>
{% endhighlight  %}

And that's it! In a few lines of HTML and JavaScript code, we've got ourselves
an app that can request the medications from the current record and display
them.
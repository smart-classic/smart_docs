---
layout: guide
title: SMART Developers Documentation
---

## Quickstart Example

Your app needs to serve, at a minimum, the following URL:

   * <http://localhost:8000/smartapp/index.html>

For this tutorial we simply use webpy to serve the static `index.html` file.  In
a real system you would typically use a webserver such as Apache to serve static
files, but `webpy's` built-in webserver works fine for demonstration purposes.


### Install Python and webpy

Depending on your environment you may need to install Python and web.py.  Follow
the [install web.py guide](http://webpy.org/install) if you need to do this.


### webpy Server Script

{% highlight python %}
import web

urls = (
    '/smartapp/index.html', 'index'
)
app = web.application(urls, globals())

class index:
    def GET(self):
        f = open('index.html', 'r')
        data = f.read()
        f.close()
        return data

if __name__ == "__main__":
    app.run()
{% endhighlight  %}

Save this script in file named `app.py` and then run it with `python app.py
8000`. It will launch a webpy's simple webserver responding to the
`http://localhost:8000/smartapp/index.html` URL by serving the content of the
`index.html` file stored in the same directory as the script. All you then need
to do is create an `index.html` file in the same directory and put the content
of your first SMART Connect app in it.


## Your First `index.html` file

The index file, served at <http://localhost:8000/smartapp/index.html> is where
all the fun happens! The first thing you need to do is to include the SMART
Javascript client library script like this:

{% highlight html %}
    <script src="http://sample-apps.smartplatforms.org/framework/smart/scripts/smart-api-client.js"></script>
{% endhighlight  %}

This script serves to connect your HTML page to the SMART JS library.

Once the client-side library has loaded, your index HTML page has access to a
SMART JS object that provides some basic context including:

<ul>
  <li><b>SMART.user</b>: which provides the name and ID of the user who
  launched the app, typically the physician logged into the SMART EMR.</li>

  <li><b>SMART.record</b>: which provides the name and ID of the patient whose
  record is currently loaded.</li>
</ul>

For a complete reference of the app context, see the [JS Library
reference](/guide/client-libs/client-js.html)

Here is an `index.html` file that fetches the name of the current patient and
give a friendly greeting. Copy this into your `index.html` file and try to
run it from `MyApp` in the developer sandbox.

{% highlight html %}
    <!DOCTYPE html>
    <html>
     <head>
      <script src="http://sample-apps.smartplatforms.org/framework/smart/scripts/smart-api-client.js"></script>
     </head>
     <body><h1>Hello <span id="name"></span></h1>

     <script>
       SMART.ready(function(){
         document.getElementById('name').innerHTML = SMART.record.full_name;
       });
     </script>
     </body>
    </html>
{% endhighlight %}

If you can see the name of the current patient in the body of your app,
congratulations, you have just written your first SMART app!


# Using the SMART API

At this point your SMART app is ready to make API calls to obtain health data.
Remember your app is contained in an IFRAME meant to access single, specific
medical record. This means you can request medical data without specifying the
patient context because the medical record has already determined by the
Javascript context.


## Asynchronous Calls

Let's load the patient's medications using `SMART.get_medications()`. The most
important thing you need to know about all SMART Javascript APIs is that they
are asynchronous: you won't get the meds as a result of the
`SMART.get_medications()` call. Instead, you need to specify callback functions
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

Go to [next steps](/guide/nextsteps.html)

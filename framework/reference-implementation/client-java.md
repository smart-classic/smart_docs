---
layout: framework
title: SMART - Java Client
---

<div class='red_box'>Note: This Java client has not been updated to the
SMART v0.6 API yet. You can continue to use it with version v0.5 of the
API.</div>


This document describes the SMART Java Client Library, which you can use from a
Java application to make authenticated REST calls into a SMART container.

You probably want to read the [SMART REST
tutorial](/guide/tutorials/smart_rest.html) first to better understand when you
might want to use this library.


## Setting Up Your Environment

To use the SMART Java client library, you need an environment in which web
requests are routed to your Java application. The most common use case is a
Web container like [Tomcat](http://tomcat.apache.org/) or
[jetty](http://jetty.codehaus.org/jetty/).

Please note that you will need Java >= 1.6.0_20 to build the SMART client
library.


## Get Code

To obtain source code you'll need `git`; to build the Java client library and
fetch dependencies, you'll also need ant >1.7. For example on Ununtu, you can:

{% highlight sh %}
  $ sudo apt-get install git
  $ sudo apt-get install ant
{% endhighlight %}

Then, grab the SMART Java client library from github:

{% highlight sh %}
  git clone https://github.com/chb/smart_client_java.git
{% endhighlight %}


## Build the JARs and a Test Servlet

On linux:

  cd smart_client_java/bin
  sh ./build.sh

Or on Windows:

  cd smart_client_java/bin
  move build.sh build.bat
  build.bat

Note that when you run the build script, it obtains dependencies using `IVY`,
which could take a few minutes. It also fetches an up-to-date copy of the SMART
ontology from <sandbox.smartplatforms.org>. If you run the the build script
multiple times, you'll be prompted to overwrite the ontology file. Just enter
`'Y'` to agree.


## Run the Test Servlet

If all went according to plan, you should find a sample RxReminder servlet built
in `build/smartapp.war`. This servlet is designed to run in the
[SMART Reference EMR Sandbox](http://sandbox.smartplatforms.org/),
and comes with the default OAuth `consumer token` and `secret` built in. You should
be able to run the sample servlet in your Web container of choice. For example, for tomcat:

 1. Copy build/smartapp.war to <tomcat-directory>/webapps
 2. Start up tomcat (on port 8000)


## Include the SMART Java Client in Your App

To write your own Java app using the SMART Java client, you'll need to include 
the following JARs in your app's `classpath`:

    build/SMArtClient.jar
    lib/*.jar


## Use the SMART Java Client in Your App

For a complete example, please see
`src/org/smartplatforms/client/tests/Reminder.java`. Here's a basic rundown of the
process:

### Import the SMART Java Client + Dependencies

The two major components you'll need to import are the SMART client libraries
and the openrdf RDF parsing/querying package:

{% highlight java %}
  import org.smartplatforms.client.SMArtClient;
  import org.smartplatforms.client.SMArtClientException;
  import org.smartplatforms.client.SMArtOAuthParser;
  import org.smartplatforms.client.TokenSecret;

  import org.openrdf.query.QueryLanguage;
  import org.openrdf.repository.RepositoryConnection;
  import org.openrdf.query.TupleQuery;
  import org.openrdf.query.TupleQueryResult;
  import org.openrdf.query.BindingSet;
{% endhighlight  %}

###Instantiate the SMART Client

When you instantiate a new `SMART Client` object, you'll need to supply an OAuth
consumer token + secret, as well as the base URL for the SMART Container. A good
approach is to define these parameters in your servlet's `web.xml` (with the
consumer token and secret set to our pre-defined "My App" values):

(but be sure to heed the warning about using the consumer_secret in
production [here](/guide/tutorials/smart_rest.html#consumer_secret_warning))

{% highlight xml %}

    <?xml version="1.0" encoding="UTF-8"?>
    <web-app xmlns="http://java.sun.com/xml/ns/javaee"
             xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
             xsi:schemaLocation='http://java.sun.com/xml/ns/j2ee/web-app_2_4.xsd
             version="">

        <description>[YOUR APP DESCRIPTION]</description>
        <display-name>[YOUR APP NAME]</display-name>

        <servlet>
            <servlet-name>smartapp</servlet-name>
            <servlet-class>[YOUR.APP.CLASS]</servlet-class>

            <init-param>
                <param-name>consumerKey</param-name>
                <param-value>my-app@apps.smartplatforms.org</param-value>
            </init-param>
            <init-param>
                <param-name>consumerSecret</param-name>
                <param-value>smartapp-secret</param-value>
            </init-param>
            <init-param>
                <param-name>serverBaseURL</param-name>
                <param-value>http://sandbox-api.smartplatforms.org</param-value>
            </init-param>
        </servlet>

        <servlet-mapping>
            <servlet-name>smartapp</servlet-name>
            <url-pattern>/*</url-pattern>
        </servlet-mapping>
    </web-app>

{% endhighlight  %}


Then, in your app's code you can say:

{% highlight java %}

  SMArtClient client = new SMArtClient(
    sConfig.getInitParameter("consumerKey"),
    sConfig.getInitParameter("consumerSecret"),
    sConfig.getInitParameter("serverBaseURL"));

{% endhighlight  %}

### Obtain access token + secret

In order to get data from a patient record, you'll need to obtain a record-based
access token and secret. For background details about how an access token and
secret are supplied to your app in the `oauth_header` URL parameter see
the [SMART REST tutorial](/guide/tutorials/smart_rest.html).

If you're responding to a `javax.servlet.doGet()` method, you can use the
following method to extract an access token and secret from the request:

{% highlight java %}
  SMArtOAuthParser authParams = new SMArtOAuthParser(req);
  TokenSecret tokenSecret = new TokenSecret(authParams);
{% endhighlight  %}

If you're not working with a `javax.servlet` request, you'll first need to your
framework's built-in tools to pull out the name and value of the authorization
header:

{% highlight java %}
    // pseudo-code
    String hval  = FIND THE HTTP GET PARAMETER CALLED "oauth_header"
    SMArtOAuthParser authParams = new SMArtOAuthParser(hval);
    TokenSecret tokenSecret = new TokenSecret(authParams);
{% endhighlight  %}

### Make a REST API Call

Now that you've instantiated a SMART client object and obtained access tokens,
you're ready to make a REST call to the SMART container. For example, you can
obtain a patient's medication list via:

{% highlight java %}
  RepositoryConnection meds = (RepositoryConnection)
  client.records_X_medications_GET(recordId, tokenSecret, null);
{% endhighlight  %}

First, note the `records_X_medications_GET` method name: it looks like the SMART
REST URL `GET /records/{record_id}/medications` but with variables replaced by
"X", and the HTTP method tacked on to the end. The parameters you pass to call
will fill in for the X's in the method name. So in the call above, the "X"
refers to a `record_id`.

Also note that the API call returns a `RepositoryConnection` object, which is an
`openrdf` object representing the SMART RDF graph.

### Work With the Results

Let's go through a simple query example here. For the complete low-down on how
to use a `RepositoryConnection` object, you can refer to the [openrdf
documentation][].

We'll use the following SPARQL query to pull out data from the
`repositoryconnection`:

{% highlight java %}
    String sparqlForReminders = "PREFIX dc:<http://purl.org/dc/elements/1.1/>\n" + 
    "PREFIX dcterms:<http://purl.org/dc/terms/>\n" +
    "PREFIX sp:<http://smartplatforms.org/terms#>\n" +
    "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n" +
    "SELECT  ?med ?name ?quant ?when\n" +
    "WHERE {\n" +
    "  ?med rdf:type sp:Medication .\n" +
    "  ?med sp:drugName ?medc.\n" +
    "  ?medc dcterms:title ?name.\n" +
    "  ?med sp:fulfillment ?fill.\n" +
    "  ?fill sp:dispenseDaysSupply ?quant.\n" +
    "  ?fill dc:date ?when.\n" +
    "}"
{% endhighlight  %}

To execute the query and iterate through results:

{% highlight java %}
  TupleQuery tq = meds.prepareTupleQuery(QueryLanguage.SPARQL, sparqlForReminders);
  TupleQueryResult tqr = tq.evaluate();

  while (tqr.hasNext()) {
    BindingSet bns = tqr.next();
    pillWhen = bns.getValue("when").stringValue();

    // .. do something with this value...
  }
{% endhighlight  %}

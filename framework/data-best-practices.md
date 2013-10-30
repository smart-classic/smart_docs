---
layout: framework
title: Best Practices for SMART Data
---

# Best Practices for Consuming SMART RDF Data

## Treat SMART data payloads as RDF

SMART Containers supply your app with medical record data in the form of an RDF
graph, with the structured specified in our data model. It's important to keep
in mind that this graph is a logical structure containing medical record data.
Yes, it's serialized as RDF/XML --- but the appropriate way to work with this
graph is by using purpose-built RDF processing tools, not generic XML processing
tools. The important concept here is you can't count on details like element
order, blank node IDs, or even XML structure to be consistent. So you shouldn't
try to use xpath or DOM manipulation to pull data out of this graph.

But you can count on the logical structure: the RDF triples asserted in the
graph. So the appropriate way to pull data from a graph is using an RDF library.
For javascript, we recommend [rdfquery](http://code.google.com/p/rdfquery/). For
Java there are several options including
[openrdf-sesame](http://www.openrdf.org/) and
[Jena](http://jena.sourceforge.net/). For Python we recommend
[rdflib](http://www.rdflib.net/). For a more comprehensive list of language
bindings, see the [w3c wiki](http://www.w3.org/2001/sw/wiki/Category:Programming_Environment).


## Use SPARQL queries to interact with SMART RDF graphs

When you retrieve data from a SMART Container, you can use SPARQL queries to
loop through results and extract relevant fields. For example, to obtain the
title and LOINC code for each lab test in the patient record, you could do

{% highlight javascript %}
    SELECT  ?lab ?labTitle ?loincCode
    WHERE {
      ?lab rdf:type sp:LabResult.
      ?lab sp:labName ?labName .
      ?labName dcterms:title ?labTitle .
      ?labName sp:code ?loincCode00.
    }
{% endhighlight  %}


## Build flexible queries to focus on the data you need

The query above works pretty well, but it doesn't do much. Let's build on it!
For example, say we want to pull out the "abnormal interpretation" flag for a
lab result. We could augment our query as follows

{% highlight javascript %}
    SELECT  ?lab ?labTitle ?loincCode ?abnormalInterpretation
    WHERE {
      ?lab rdf:type sp:LabResult.
      ?lab sp:labName ?labName .
      ?labName dcterms:title ?labTitle .
      ?labName sp:code ?loincCode00.
      ?lab sp:abnormalInterpretation ?abnormalInterpretation.
    }
{% endhighlight  %}

But now something funny happens: if some lab results are missing the "abnormal
interpretation" flag, this SPARQL query won't find them! That's because we've
build a rigid query that requires each field to be present. If we want to query
in a more flexible way, we can use the OPTIONAL keyword

{% highlight javascript %}
    SELECT  ?lab ?labTitle ?loincCode ?abnormalInterpretation
    WHERE {
      ?lab rdf:type sp:LabResult.
      ?lab sp:labName ?labName .
      ?labName dcterms:title ?labTitle .
      ?labName sp:code ?loincCode00.
      OPTIONAL { ?lab sp:abnormalInterpretation ?abnormalInterpretation.}
    }
{% endhighlight  %}

Now if some labs have an "abnormal interpretation" flag, we'll find it. But we
won't ignore labs that happen to be missing that field: we'll still get their
LOINC codes and be able to keep track of them.

Because not every SMART data element will provide a value for every field, it's
important to keep your queries flexible with OPTIONAL blocks, focusing on the
data you need and layering on additional data that might be useful, but isn't
essential.


## Parse date fields as [W3C datetime / ISO-8601  strings](http://www.w3.org/TR/NOTE-datetime)

Let's say you're building a timeline application that displays the dates of
medication fulfillments. You make a SMART API call to get a list of
fulfillments, you write a SPARQL query to pull out the dates, and now you're
ready to plot them. It's important to treat dates as [W3C datetime / ISO-8601](http://www.w3.org/TR/NOTE-datetime) strings without making further
assumptions about their format. For example, depending on the granularity of
data available, one fulfillment might have the date "2011-06-12", while another
might have the date "2011-06-12T18:30Z". If you try to parse SMART date fields
with a simple regular expression or by substring-matching, you'll have trouble
maintaining the flexibility you need. Instead, you should use a library that
handles ISO8601 dates. For javascript we'd recommend reading [this for background](http://delete.me.uk/2005/03/iso8601.html). And we'd recommend trying
the [xdate.js](http://arshaw.com/xdate/) library for a powerful set of
cross-platform date-parsing and arithmetic tools. Most other languages have
standard libraries for parsing ISO8601 dates.

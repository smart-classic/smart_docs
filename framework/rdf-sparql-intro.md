---
layout: framework
title: SMART - Quick Introduction to RDF and SPARQL
---

## A Quick Introduction to RDF and SPARQL


The SMART API supplies patient record data in the form of an RDF graph. If
you've never used (or even heard of!) RDF, this document should help you get up
to speed. So let's jump right in!


### What is RDF, anyway?

RDF, the Resource Description Framework, is a web standard "for representing
information about resources" (this according to the [W3C's RDF
Primer](http://www.w3.org/TR/2004/REC-rdf-primer-20040210/)). In brief, it's a
flexible way to represent data in the form of sentences or "triples" that link
a subject, a predicate, and an object. For example, let's say we want to
represent the idea that "Mr. Smith takes atorvastatin". We might create the
following triple

* subject Mr. Smith
* predicate takes
* object atorvastatin


There are two key ideas here

<ol><li>Everything (almost) is a resource.</li>
    <li>Resources are related by triples</li>
</ol>

Let's explore each in more depth


### Everything (almost) is a resource

In RDF, every triple has a resource as its subject. In our example, we call Mr.
Smith a "resource" because he is a particular guy out there in the world. He is
not just the string of letters "M-r-.-S-m-i-t-h." Importantly, if I know Mr.
Alex Smith and you know Mr. Bob Smith, we are not talking about the same
resource! To prevent these kinds of mix-ups, resources in RDF aren't just
identified by strings like "Mr. Smith." Instead, they're represented by Uniform
Resource Identifiers basically URLs that provide a built-in namespace. For
example, let's say my Mr. Smith maintains a web site at
[http://alexsmith.somedomain.com](http://alexsmith.somedomain.com). I might
refer to him by the URL
[http://alexsmith.somedomain.com/me](http://alexsmith.somedomain.com/me]). Now
you certainly wouldn't confuse my Mr. Smith for yours! (Note there doesn't have
to be an actual web page served at the address of a URI. The important thing is
that the URI identifies a resource. Uniformly.)

What about the predicate in our example, the word "takes"? Predicates in RDF
are triples, too. If we just used the string "takes" as our predicate, again we
might mean different things I might mean "consumes a drug, as part of a daily
regimen", and you (cynic!) might mean "steals from his wife's pillbox on
Thursday mornings." To resolve this ambiguity, I could represent 'takes' as
[http://joshuamandel.com/my_drug_vocabulary/takes](http://joshuamandel.com/my_dr
ug_vocabulary/takes). Over time, I could build up a rich vocabulary with all
kinds of terms, and use these as predicates in my RDF triples. In general,
things work best when people can agree on the meanings of terms and use a
shared vocabulary. So folks build up publically defined vocabularies such as
[FOAF](http://xmlns.com/foaf/spec/) (used to describe the elements in social
networks like friends, names, and birthdays) or [Dublic
Core](http://purl.org/dc/elements/1.1/) (used to describe metadata like the
Titles, Creators, and Publishers or resources). These shared vocabularies
become the basis for rich representation (and interpretation) of information
about resources.

And finally, what about "atorvastatin"? Again, the best way to represent a
concept like atorvastatin is as a URI that everyone can agree on. One
possibility is to use the drug's RxNorm Concept ID (in this case, 83367) as
part of the URI. For example, SMART uses the URI
[http://link.informatics.stonybrook.edu/rxnorm/RXCUI/83367](http://link.informat
ics.stonybrook.edu/rxnorm/RXCUI/83367), sharing a vocabulary with Stonybrook.
But recall we said almost everything is a resource. If we want, RDF lets us use
a simple string as the object of a triple. So, for example, consider this
representation of a Haiku

* subject [http://dilute.net/poems/25](http://dilute.net/poems/25)
* predicate dcterms title (Dublin Core Terms vocabulary's 'title' predicate)
* object "Haiku entitled Substitutability the SMART way to go."

In this case, I don't need to point to a resource as the title of my haiku. The 
title is really just a string, after all -- so I can just represent it as such. 


### Resources are related by triples

In RDF, the only way to represent relations among resources is by creating
triples. If graph theory is your thing, you can think of triples as arcs in a
directed graph from subject to predicate to object. The same resource can be
the subject (or object) or multiple triples. For example, consider my SMART
haiku.  In addition to the triple above, I could some more triples

* subject [http://dilute.net/poems/25](http://dilute.net/poems/25)
* predicate dc:creator (Dublin Core vocabulary's 'creator' predicate)
* object [http://joshuamandel.com/me](http://joshuamandel.com/me)


* subject [http://joshuamandel.com/me](http://joshuamandel.com/me)
* predicate foaf:name (FOAF vocabulary's 'name' predicate)
* object "Josh Mandel"

Note that I am the object of one triple (as the creator of the haiku) and the
subject of another (as a person with a name)!

What about more complex relationships? For example, what if I want to represent
the fact that my breakfast this morning consisted of Joe's O's, milk, and
coffee? This is an open-ended data-modeling exercise, but I'll just point out
one approach which involves creaing a resource for "the stuff I had for
breakfast this morning", and adding relations to that. So then (in sketch form)
we'd have

* subject http://joshuamandel.com/me
* predicate http://joshuamandel.com/my_food_vocabulary/ate
* object stuff-I-ate-this-morning


* subject stuff-I-ate-this-morning
* predicate rdfli (RDF vocabulary's 'list item' predicate)
* object "Joe's O's"

* subject stuff-I-ate-this-morning
* predicate rdf li
* object "milk"


* subject stuff-I-ate-this-morning
* predicate rdf li
* object "coffee"

Notice that I've loosely referred to a resource here as the "bunch of stuff I
ate this morning". I didn't give it a formal URI, because it doesn't exist
outside of the context of this particular RDF graph, and it's entirely defined
by its relations above. For cases like this, RDF provides anonymous or blank
nodes whose identifiers have meaning only within the context of a particular
graph.


### Representing RDF Graphs

So far, we've been talking about RDF graphs as theoretical sets of triples. How
do we write down or "serialize" an RDF graph in a way that lets us share it
with others? There are in fact several standard notations for representing an
RDF graph. The simplest representation is to write triples out, one per line,
with a period at the end of each line. URIs are enclosed in angle brackets
(e.g.  \<[http://my_uri](http://my_uri)>\; blank nodes are prefaced with the _
prefix (e.g. &#95;my-blank-node), and strings are enclosed in quotes (e.g. "my
string value")

<http://dilute.net/poems/25> <http://purl.org/dc/terms/title> \"Haiku entitled /
Substitutability: / the SMART way to go.\" .

An XML-based representation known as RDF/XML serializes the same triple more
verbosely:

{% highlight html %}
<?xml version="1.0"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
xmlns:terms="http://purl.org/dc/terms/">
    <rdf:Description rdf:about="http://dilute.net/poems/25">
        <terms:title>Haiku entitled /  Substitutability: / the SMART way to 
go.</terms:title>
    </rdf:Description>
</rdf:RDF>
{% endhighlight  %}



## And what about SPARQL?

SPARQL is a query language for interacting with RDF graphs. The syntax is
designed to look a bit like SQL, the structured query language used with
relational databases. The W3C maintains an [extremely
readable](http://www.w3.org/TR/rdf-sparql-query/) standard that's peppered with
examples. Here, we'll not even skim the surface...


### A simple SPARQL query

Given our breakfast graph above, let's write a query to find all the things I
ate! Here's a first attempt (not quite perfect)

    PREFIX food: <http://joshuamandel.com/my_food_vocabulary/> 
    SELECT ?f WHERE
    {
      <http://joshuamandel.com/me> food:ate ?f.
    }


A bit of syntax I've defined a prefix called "food" which I'll use to refer to
my personal food vocabulary. This is just for readability; it lets me later
write food:ate instead of the more verbose
[http://joshuamandel.com/my_food_vocabulary/ate](http://joshuamandel.com/my_food
_vocabulary/ate).

Now here's what the query does: it looks for triples that match the pattern
inside the WHERE clause. In this case, triples whose subject is me; whose
predicate is food:ate and whose object can be anything (indicated by the
question mark in ?f). My decision to use ?f as a variable name was completely
discretionary. I could have called it ?nourishment or ?xyzzy. The name only
matters within the context of my query.

But this query has a problem it returns the blank node
stuff-I-ate-this-morning -- and not the actual foods! Let's fix it by adding
to our WHERE clause

    PREFIX food: <http://joshuamandel.com/my_food_vocabulary/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    SELECT ?individual_food WHERE
    {
      <http://joshuamandel.com/me> food:ate ?bunch_of_food.
      ?bunch_of_food rdf:li ?individual_food.
    }

Now our where clause includes two statements we're looking for individual foods
that are items in the list of foods eaten by me. In other words, now we're
drilling down into the bunch of food to pull out individual items! This returns
a list of three bindings for the ?individual&#95;food "coffee", "milk", and "Joe's
O's".

This was just the briefest introduction to the anatomy of a SPARQL query. For
lots more specific examples, try SPARQL examples for SMART.

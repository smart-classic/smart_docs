---
layout: models-reference
title: SMART Data Models
---

## SMART Data Models

<div class="well">
  <p>N.B. This is highly preliminary, not a commitment or final
  version of any particular API or data model. This is purely
  for internal collaboration and preview purposes.</p>
</div>


### RDF Overview

SMART API calls return data in the form of RDF graphs. Within these graphs,
top-level SMART data objects have fully dereferenceable URIs. For instance,
let's consider a SMART-enabled EMR hosted with its API base at
<http://sample_smart_emr.com/smart-app/>. An individual medication in this EMR
might be retrievable via:

    GET http://sample_smart_emr.com/smart-app/records/123456/medications/664373).

When you issue a GET request for a top-level SMART object like a medication,
you'll receive a graph containing:

1. The object itself
2. All properties linking it to "core data" elements (such as a medication's `drugName`,
   which is a `CodedValue` node)
3. All properties linking it to other top-level SMART objects
4. All "core data" elements belonging to the elements in (3)

For instance, when you `GET` a medication, you'll get all the information about
that medication and any fulfillments that belong to it! Likewise, when you `GET`
a fulfillment, you'll get all the information about that fulfillment and the
medication to which it belongs.

Another way to say this is: when you make an API call for data, the graph you
receive goes one top-level SMART element deep.


### Important note: RDF/XML Serializations are not unique!

It's important to understand that SMART API calls return RDF graphs [RDF/XML][]
&mdash; and for a given graph, there are _multiple_ possible serializations. We
don't make guarantees about how a graph will be serialized, beyond saying that
it's valid RDF/XML. So to consume the SMART API, you should parse the RDF/XML
payloads as RDF/XML &mdash; for example, `don't` try to query them directly with
xpath!

[RDF/XML]: http://www.w3.org/TR/REC-rdf-syntax/

To give a concrete example, a medication might be serialized as:

    <sp:Medication>
      ... { additional properties here }....
    </sp:Medication>

Or you could see the equivalent:

    <rdf:Description>
          <rdf:type rdf:resource="http://smartplatforms.org/terms#Medication"/>
      ... { additional properties here }....
    </rdf:Description>

### Namespaces

A common set of namespace prefixes is used for the examples below. These are:


<table class="table table-striped">
  <caption align="bottom">RDF Namespaces</caption>
  <tr>
    <td>dcterms</td>
    <td><a href="http://purl.org/dc/terms/">http://purl.org/dc/terms/</a></td>
    <td>Dublin core terms</td>
  </tr>
  
   <tr>
    <td>foaf</td>
    <td><a href="http://xmlns.com/foaf/0.1/">http://xmlns.com/foaf/0.1/</a></td>
    <td>Friend of a friend</td>
  </tr>

   <tr>
    <td>rdf</td>
    <td><a href="http://www.w3.org/1999/02/22-rdf-syntax-ns#">http://www.w3.org/1999/02/22-rdf-syntax-ns#</a></td>
    <td>Resource description framework</td>
  </tr>

  <tr>
    <td>sp</td>
    <td><a href="http://smartplatforms.org/terms#">http://smartplatforms.org/terms#</a></td>
    <td>Smart platforms root namespace</td>
  </tr>

  <tr>
    <td>v</td>
    <td><a href="http://www.w3.org/2006/vcard/ns#">http://www.w3.org/2006/vcard/ns#</a></td>
    <td>vCard namespace</td>
  </tr>
</table>


### Naming Conventions in the SMART Ontology

We use the prefix `sp` to designate the <http://smartplatforms.org/terms>
namespace. Within this namespace, we use a simple convention to differentiate 
between classes and predicates:

* Class names are designated by `CamelCase` with a capitalized first character.
  Examples: `sp:Medication` and `sp:LabResult`.

* Predicate names are designated by `camelCase` with a lower-case first character.
  Examples: `sp:medication` or `sp:valueAndUnit`.

You may wonder why classes and predicates tend to have similar names. For
example, we define a class `sp:Medication` as well as a predicate `sp:medication`.
Here's why: a predicate like `sp:medication` is used to indicate that a clinical
statement is associated with a medication; a class like `sp:Medication` is used to
indicate that a clinical statement is a medication. For example, each
`sp:Fulfillment` statement is associated with a `sp:Medication` statement via the
predicate `sp:medication`. This makes sense when we consider a few RDF triples
that expresses the basic pattern, associating a fulfillment with its medication
via the `sp:medication` predicate

    _:f123 rdf:type sp:Fulfillment.   # declares a Fulfillment statement
    _:m456 rdf:type sp:Medication.    # declares a Medication statement
    _:f123 sp:medication _:m456.      # links the Fulfillment to its Medication


<hr>

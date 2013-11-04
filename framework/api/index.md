---
layout: api-reference
title: SMART REST API
---

# SMART REST API Overview

<div class="well">
  <p>N.B. This is highly preliminary, not a commitment or final
  version of any particular API or data model. This is purely
  for internal collaboration and preview purposes.</p>
</div>


The SMART API provides access to individual resources (medications, fulfillment
events, prescription events, problems, etc.) and groups of these resources in a
[RESTful][] API.

[RESTful]: http://en.wikipedia.org/wiki/Representational_state_transfer


## REST Design Principles

In general you can interact with a:

* Group of resources using:
  * `GET` to retrieve a group of resources such as `/medications/`
* Single resource using:
  * `GET` to retrieve a single resource such as /medications/{medication_id}


## OWL Ontology File

The API calls listed below, as well as the RDF/XML payloads, are also
defined in a machine-readable OWL file. The OWL file has been used to
generate the documentation below, as well as our client-side REST
libraries and API Playground app.


## Call Scopes

Each `GET` call in the SMART REST API is listed below and grouped by the
"scope" or "access control category" the SMART container applies to the
call. The SMART container implements this access control using the OAuth
tokens passed in with each API request as described in the [build a REST
App howto][]. TODO

[build a REST app howto]: /howto/build_a_rest_app/

Currently there are three "scopes" or access control categories:

1. `Container` calls can be made by anyone against the container.
   Examples of this type of call are fetching the container's manifest
   and fetching the container's ontology.  These calls need not
   be OAuth-signed (though it is not incorrect to sign them).

2. `Record` calls are scoped to a (app, user, record) tuple e.g. calls
   to fetch a patient's medical record data. An example would be getting
   the medications in a patient's record. The OAuth credentials for
   the app (e.g. the `consumer_key` and `consumer_secret`) and
   previously fetched OAuth credentials from the server including the
   `smart_record_id` These calls must be signed as "3-legged" 
   OAuth requests, meaning they are signed with a combination of
   the app's consumer token + access token.

3. `User` calls are scoped to a (app, user) tuple and are used for
   setting a user's preferences _for that app only_. These calls are also
   signed as "3-legged" OAuth calls, using an app's consumer token +
   access token. (Future versions of the SMART API may allow an app to 
   read another's preferences or add a "global" set of user preferences.) 


## Filters

The SMART API offers a basic filtering capability to narrow down large clinical
statement result sets on the server before returning data to the client. As of
SMART 0.6, for all API calls that return multiple SMART Clinical Statements
(e.g. `GET /records/xxx/lab_results`), you can attach date filters if relevant
to the returned data type, and in a few select cases other datatype specific
filters (such as LOINC codes on lab results) as URL parameters.


### Common Date Filters

All SMART API calls for clinical statements that have a `date` or `startDate`
attribute can now be filtered on those attributes by sending the following
query parameters in the request.

Note: even if the data includes an `endDate`, it is not used by any of
the current filters.

- `date_from`
- `date_from_excluding`
- `date_from_including`
- `date_to`
- `date_to_excluding`
- `date_to_including`


### Statement Specific Filters

The following calls have additional filters:

* [Lab Results](/framework/models/#Lab_Result): `loinc` &mdash; a
pipe-separated LOINC codes. e.g. `loinc=29571-7|38478-4`

* [Vital Sign Sets](/framework/models/#Vital_Sign_Set): `encounter_type`
  &mdash; a pipe-separated encounter types. e.g. `encounter_type=ambulatory`

* [Medications](/framework/models/#Medication): `rxnorm` &mdash; a
  pipe-separated list of RXNORM codes. e.g. `rxnorm=856845`

* [Problems](/framework/models/#Problem): `snomed` &mdash; a pipe-seperated
  list of SNOMED codes. e.g. `snomed=161891005`

* [Procedures](/framework/models/#Procedure): `snomed` &mdash; a
  pipe-seperated list of SNOMED codes. e.g. `snomed=161891005`


### Default Sort Order and Paginating Results

Each SMART API call that returns sets of Clinical Statements now have a default
sort order defined for them based on either the `date` or `startDate`
attribute. The previously defined `offset` parameter has been removed. This
requires a change in an app's pagination strategy to use date filters, the
`limit` parameter, and the metadata in the `ResponseSummary` to paginate
results.  See also `resultsReturned` and `totalResultCount` in the
`ResponseSummary` object in the next section.

The default behavior of any call is to return all results, if no limit is
supplied in the request.

### Response Summary

To complement the filtering and pagination API, each query response
includes a simple `api:ResponseSummary` object that looks like this:

    <rdf:Description rdf:nodeID="Naa3f4ca7b6024d6ab616aa31fa5ab528">
        <api:processingTimeMs rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">19</api:processingTimeMs>
        <rdf:type rdf:resource="http://smartplatforms.org/terms/api#ResponseSummary"/>
        <api:resultsReturned rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">2</api:resultsReturned>
        <api:totalResultCount rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">2</api:totalResultCount>
        <api:resultOrder rdf:nodeID="Nff3cac65263543dfa82450b51355c031"/>
      </rdf:Description>


### An Javascript Example for Filtering Lab Results

For this example, we'll be using the SMART JSON-LD interface described
[here](/framework/json-ld.html) to the SMART Connect Javascript library.

To start let's set up a query with the following parameters:

- Filter the labs to find this patient's LDL results. LDL's have three
  LOINC codes that differ only in the method used to find the result. We'll
  make a pipe (|) seperated string of these codes: `"13457-7|2089-1|18262-6"`

- Find the results from 2010-01-01 to 2012-01-01 using the `"date_from"`
  and `"date_to"` parameters.

- Lastly, let's restrict the number of returned results to a "page" of
  10 results by setting the `limit` parameter to `10`. To fetch the next
  "page" of ten results, your code would update the `date_from` query
  parameter to the value of the last result returned from the previous
  call and keep the limit at `10`.

The parameters above are passed to the `get_lab_results` call as
a standard Javascript object and the results are passed to your
callback function in the same way as the other API calls:

{% highlight javascript %}
    SMART.get_lab_results({
        'date_from': '2010-01-01',
        'date_to':   '2012-01-01',
        'loinc':     '13457-7|2089-1|18262-6',
        'limit':     10,
        'offset':    0
    }).then(function(r){
        var ldls = r.objects.of_type.LabResult;
        $.each(ldls, function(i, ldl){
            // ouput each lab to the console
            var date = ldl.dcterms__date;
            var value = ldl.quantitativeResult.valueAndUnit.value;
            var unit = r.quantitativeResult.valueAndUnit.unit;
            console.log('LDL result: ', date, value, unit);
        })

        // view the responseSummary object
        var rs = r.objects.of_type.ResponseSummary;
        console.log('resultsReturned', rs.resultsReturned);
        console.log('totalResultCount', rs.totalResultCount);
        console.log('nextPageURL', rs.nextPageURL);
    })
{% endhighlight %}


## Preferences and Scratchpad API

The SMART preferences and scratchpad APIs provide a facility that SMART apps
can use to persist data about the application and user preferences, notes about
the patient record, and other pertinant data. While the two APIs are similar,
they have different intent and therefore a different scope. In both instances,
SMART does not mandate a speific format for the data stored, only that it can
be serialized in unicode. Each app is responsible for choosing an appropriate
serialization format for its data.

### Preferences API

The preferences API provides a way for your app to store data within the SMART
container automatically scoped on per user and app basis. The data can be
stored in any format that makes sense to the app. In the SMART Connect client,
you can now call the `get_user_preferences`, `put_user_preferences`, and
`delete_user_preferences` methods. For the put methods you will have to provide
a MIME content type for the data that you are storing within the container.

### Scratchpad API

The SMART 0.6 Scratchpad API enables SMART apps to store data pertaining to a
patient record in free form format. This is, the app decides on the format of
the data that it wants to store (self-structured) making the data opaque to the
container. All SMART apps are allowed read access to the scratchpad data for
the in-scope patient of all other apps, which provides a basic interoperability
facility accross apps.

Because a SMART app has access to the scratchpad that it owns regardless of the
user who runs it, there is always the possibility that a user overwrites the
data stored by another user. A container is free to implement collision
detection support for its scratchpad facilities.

*Note:* The SMART reference implementation scratchpad is not collision-safe.
Data may be lost by multiple copies of an app trying to write in parallel.
Production implementations are encouraged to implement a system that will, for
example, provide locks and dirty-state notification via HTTP error codes to
apps writing to the scratchpad.


<br> <br> <br>


# The API

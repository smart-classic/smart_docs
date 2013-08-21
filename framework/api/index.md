---
layout: api-reference
title: SMART REST API
---

## SMART REST API

<div class="well">
  <p>N.B. This is highly preliminary, not a commitment or final
  version of any particular API or data model. This is purely
  for internal collaboration and preview purposes.</p>
</div>


### Overview

The SMART API provides access to individual resources (medications, fulfillment
events, prescription events, problems, etc.) and groups of these resources in a
[RESTful][] API.

[RESTful]: http://en.wikipedia.org/wiki/Representational_state_transfer


### REST Design Principles

In general you can interact with a:

* Group of resources using:
  * `GET` to retrieve a group of resources such as `/medications/`
* Single resource using:
  * `GET` to retrieve a single resource such as /medications/{medication_id}


### OWL Ontology File

The API calls listed below, as well as the RDF/XML payloads, are also
defined in a machine-readable OWL file. The OWL file has been used to
generate the documentation below, as well as our client-side REST
libraries and API Playground app.


### Call Scopes

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

---

* Query Filters
* OAuth Guide

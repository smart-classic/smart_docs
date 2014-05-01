---
layout: smart_on_fhir
title: SMART on FHIR -- Clients -- JavaScript
---

# SMART on FHIR: JavaScript Client Library

## Getting started

The SMART on FHIR JavaScript client library helps you build browser-based SMART
apps that interact with a FHIR REST API server. It can help your app get
authorization tokens, provide information about the user and patient record in
context, and issue API calls to fetch clinical data.

To get started with the SMART on FHIR JavaScript client library, you'll need to:

### 1. Include a `script` tag

Include a `script` tag referencing the library. The latest code is always
available in GitHub at
[jmandel/fhir-js-client ](https://raw.githubusercontent.com/jmandel/fhir-js-client/master/dist/fhir-client.js).

You'll want to download and host this file alongside your app, unless you're
just prototyping.

Including this script creates a global `FHIR` object for you to work with.

### 2. Create or obtain an instance of `FHIR.client`

In a typical workflow, you won't instantiate this object yourself -- it will
be created by `FHIR.oauth2.launch()`. But when you're prototyping, you can just
create your own. By convention, we call this instance `smart`. So you can
create a client via:

```
var smart = FHIR.client({
  fhirServiceUrl: 'https://open-api.fhir.me',
  patientId: '1137192'
});
```

This object will be your touchpoint for making FHIR API calls. Your client
will have some context built in, including:

* `smart.context.patient`
* `smart.context.practitioner`

### 3. Use your client instance to execute FHIR API calls

You can make calls like:

* `read`: fetch a single resource, given its id
* `search`: search for resources that match a set of criteria

In general, you can make API calls thare are scoped to the current patient by
using `smart.context.patient`, as follows:

```
// Search for the current patient's conditions
smart.context.patient.Condition.search();

// Search for the current patient's prescriptions
smart.context.patient.MedicationPrescription.search();
```

If you're writing a population-level app, you can query across patient records
by using `smart.api`, as follows:

```
// Search for the all conditions added today
var todaysDiagnoses = smart.api.Condition.where.dateAsserted("2014-05-01").search();

// Search for all statins prescribed today
var statinRxs = smart.api.MedicationPrescription.where
  .datewritten("2014-05-01")
  .medication(smart.api.Medication.where
    .name("statin")
  ).search();
```

These functions return `$.Deferred` objects, which you can work with simply by
calling their `done` method:

```
statinRxs.done(function(prescriptions, cursor){
  console.log(prescriptions[0]);
});
```

In the `done` callback, you'll get an array of search results, and potentially
a paging cursor that you can use to fetch the next page of results. To use the
cursor, just call `cursor.next()`, which gives you a new `Deferred` result set.

Here's a complete example of the steps above:

TODO <!-- plunkr iframe embed -->

## Supported API operations

The JS client supports the following FHIR API calls:

#### Instance-level operations

* `read`  Read the current state of a given resource
* `vread` Read a specific version of a given resource

#### Type-level operations

* `search` Search for resources of a given type that match a set of filters

For full deatils on these operations, the FHIR API calls are documented at:
http://www.hl7.org/implement/standards/fhir/http.html

## Reading a single resource: instance-level operations

Instance-level operations in FHIR work with a single resource instance at a
time. Two key operations are `read` and `vread`:

  * `smart.api.Something.read(resourceId)`  Read the current state of a given resource
  * `smart.api.Something.vread(resourceId, versionId)`  Read a sepcific version of a given resource

Just change `Something` to the name of a FHIR resource from [this complete
list](http://www.hl7.org/implement/standards/fhir/resourcelist.html). The
resources you can work with include:

* `AllergyIntolerance`
* `MedicationPrescription`
* `MedicationDispense`
* `Medication`
* `Observation`
* `Patient`
* `Procedure`

## Searching for resources: type-level operations

The most important type-level operation is `search`, which allows you to find
resources of a given type, with a set of filters applied.

To search for resources you'll use either:

 * `smart.api.Something.search()`  when you want to search across patients, or

 * `smart.context.patient.Something.search()` when you only want results for the patient in context.

(Note: that in any case your app will only be able to read the data it's
authorized to see -- so you could be lazy and query for "all" the data knowing
that authorization restrictions will limit what you see. But it's a good
practice to write explicit patient-level queries when that's what you have in
mind, because it will make your intentions more clear -- and make your code
more portable.)

### FHIR Search Parameters

When you perform a FHIR `search` operation, you'll often want to specific
filters to limit the results you get back. For example, you may want to get a
list of HbA1c lab results, and you're not interested in cholesterol readings.
You can create an expressive set of filters using FHIR's "search parameters," a
set of constraints passed along as URL parameters. The SMART on FHIR JS client
has built-in support for all search parameters defined in FHIR. To learn how
these work, let's take the `MedicationPrescription` resource as an example.
FHIR [defines a set of search
parameters](http://www.hl7.org/implement/standards/fhir/medicationprescription.html#search)
for this resource (and all other resources) at the bottom of the resource documentation page. Within the FHIR spec, we see:

<table class="list">
<tr><td><b>Name</b></td><td><b>Type</b></td><td><b>Description</b></td></tr>
<tr><td>_id</td><td><a href="http://www.hl7.org/implement/standards/fhir/search.html#token">token</a></td><td/></tr>
<tr><td>datewritten</td><td><a href="http://www.hl7.org/implement/standards/fhir/search.html#date">date</a></td><td>Return prescriptions written on this date</td></tr>
<tr><td>encounter</td><td><a href="http://www.hl7.org/implement/standards/fhir/search.html#reference">reference</a></td><td>Return prescriptions with this encounter identity</td></tr>
<tr><td>identifier</td><td><a href="http://www.hl7.org/implement/standards/fhir/search.html#token">token</a></td><td>Return prescriptions with this external identity</td></tr>
<tr><td>medication</td><td><a href="http://www.hl7.org/implement/standards/fhir/search.html#reference">reference</a></td><td>Code for medicine or text in medicine name</td></tr>
<tr><td>patient</td><td><a href="http://www.hl7.org/implement/standards/fhir/search.html#reference">reference</a></td><td>The identity of a patient to list dispenses  for</td></tr>
<tr><td>status</td><td><a href="http://www.hl7.org/implement/standards/fhir/search.html#token">token</a></td><td>Status of the prescription</td></tr>
</table>

In short, this defines the set of paramters that can be used to search for a
prescription. Each parameter has a name, which is how we refer to it, and a
type, which tells us what kind of operations it supports. For example,
`date`-type search parameters like `datewritten` allow simple date math like:

```
// Written anytime in the year 2014 and still active
smart.api.MedicationPrescription
  .where
  .status("active")
  .datewritten("2014")

// Written between January 2014 and December 2015
smart.api.MedicationPrescription
  .where
  .datewritten(">=2014")
  .datewritten("<2016")
```

These examples raise a few key points:

1. You introduce a set of search filters using the `.where` operation.

2. The FHIR search parameter names are directly translated into JS function
names. To preserve compatibility with JS naming rules, FHIR parameter names
with dashes, like `value-quantity`, are convereted to camel-cased names like
"valueQuantity".

3. Multiple search filters can be chained together. These act like "and"
operations -- so  in the example above, we'll only match prescriptions whose
date was after the beginning of 2014 *and* before the beginning of 2016.

You can also query for  the *or* of two values, also known as a "disjunction".
For example, say you want to find all patients named "John Smith" *or* "Bob
Smith". To search by disjunction, just add `In` to a search parameter name.
This looks like:

```
smart.api.Patient.where
  .givenIn("John", "Bob")
  .family("Smith")
```

(Note: you can pass multiple arguments, or array arguments like
`givenIn(["John", "Bob"])` -- these work identically.

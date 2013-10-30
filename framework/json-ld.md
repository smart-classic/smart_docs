---
layout: framework
title: The SMART JSON-LD API
---

# The SMART JSON-LD API

The SMART JSON-LD API provides an additional interface to the SMART datamodel
based on Javascript objects in addition to the RDF/XML and the SPARQL
interface. SMART's RDF-based interface will remain available for use as well.

# What is JSON?

[JSON][] is the highly popular lightweight data serialization and
interchange format based on a simplified subset of Javascript objects.  It's a
natural fit for representing data for SMART Connect apps. All JSON objects are
valid Javascript objects so all Javascript tools and libraries &mdash;
including tools already built into most browsers &mdash; can be used to examine
and manipulate them. We'll see examples of this below.

[JSON]: http://json.org


# What is JSON-LD?

[Linked Data][] is the idea that to be truly useful data should be
described in 1) standardized formats and 2) should be linked to other
data via identifiers that 3) could be "fetched" to find data that contains
further links to be fetched _ad infinitum_. In essence, a "web of data".
[JSON-LD][] is a leading standard to represent linked data in JSON.

As a SMART app developer, you don't have to be concerned with creating
JSON-LD objects or even querying for them, since the SMART JavaScript
client library will provide you with JSON-LD objects automatically
each time you make usual API calls like `get_MEDICATIONS()`.

[Linked Data]: http://en.wikipedia.org/wiki/Linked_data
[JSON-LD]:     http://json-ld.org


# A SMART JSON-LD Object

Here is a simplified example of the SMART `get_medications` API call
returning a JSON-LD Object as used by the SMART Diabetes Monograph app:

{% highlight javascript %}
    // Define a callback for the SMART.get_medications() API call
    SMART.get_medications().then(function(r){

      // All the JSON-LD data is in "r.objects". Here we select
      // the list of medications and iterate over them
      _(r.objects.of_type.Medication).each(function(m){

        // Each medication (m) has a startDate, drugName, and
        // instructions as required by the SMART datamodel. We
        // push a new array object on to the existing pt.meds_arr array
        pt.meds_arr.push([
          new XDate(m.startDate).valueOf(),
          m.drugName.dcterms__title,
          m.instructions
        ])
      })
    })
{% endhighlight %}

Looking into the first object in the `r.objects.of_type.Medication` array in a
browser's developer tools (such as Chrome's Developer Tools or Firebug) you can
see that it is a standard JSON object filled with the patient's data according
to the SMART data model for a [medication][].

[medication]: http://dev.smartplatforms.org/reference/data_model/#Medication

{% highlight javascript %}
    // simplified to show only relevant properties
    r = {
      "objects": {
        "of_type": {
          "Medication": [
            {
              "drugName": {
                "code": {
                  "dcterms__identifier": "200345",
                  "dcterms__title": "Simvastatin 80 MG Oral Tablet",
                  "system": "http://purl.bioontology.org/ontology/RXNORM/"
                },
                "dcterms__title": "Simvastatin 80 MG Oral Tablet"
              },
              "instructions": "1 qhs",
              "startDate": "2008-01-05"
            }
          ]
        }
      }
    }
{% endhighlight %}

## The SMART Convention for Property Names

There is a strict correspondence between the [SMART datamodel][] and the
naming of the properties of SMART JSON-LD objects. In the example above,
`drugName` is defined as containing a `Coded Value` where the `code`
property is constrained to come from `RxNorm_Semantic`. (`RxNorm_Semantic`
is furthed defined in the SMART datamodel.) `Coded Values` have two required
properties: `title` (defined by http://purl.org/dc/terms/title i.e. a the
`title` term from the Dublin Core namespace) and a `code` object from the SMART
namespace.

[SMART datamodel]: http://dev.smartplatforms.org/reference/data_model/

In SMART we namespace property names using a simple convention: first our
SMART-specific "short" name of the namespace (e.g. `dcterms`
for the Dublin Core Terms namepsace), then _two_ underscore characters,
then the property name itself. Properties in the SMART namespace are
represented directly, without underscores.  In other words, any property
without a namespace is in the SMART namespace (`http://smartplatforms.org/terms#`).

The [code][] object is defined by the SMART datamodel as having three
required properties:

1. an `identifier` defined by <http://purl.org/dc/terms/identifier>
2. a `title` defined as above
3. a `system` defined by SMART to be a literal URI reference to the
   coding system that defines the `identifier`. In this case the
   `system` is a URI for the RXNORM drug vocabulary.

[code]: http://dev.smartplatforms.org/reference/data_model/#Code


# A Complete Example: Got Statins? with JSON-LD

Here is a rewrite of the [Got Statins?][] app using the SMART JSON-LD API
improvements from the original RDF/XML and SPARQL version are noted in
the comments.

{% highlight html %}
<!DOCTYPE html>
<html>
  <head>
    <title>Got Statins?</title>
  </head>
  <body>
    <h1 style="font-family: Arial, sans-serif;">Got Statins?</h1>
    <a id="TheAnswer">...</a>

    <script src="http://sample-apps.smartplatforms.org/framework/smart/scripts/smart-api-client.js"></script>
    <script>
      SMART.ready(function(){
        SMART.get_medications().success(function(r) {

          // The (old) SPARQL query for getting the medlist
          // var medlist = meds.graph
          //                   .where("?m rdf:type sp:Medication")
          //                   .where("?m sp:drugName ?dn")
          //                   .where("?dn dcterms:title ?drugname");

          // The JSON-LD property lookup for getting the medlist
          var medlist = r.objects.Medication;

          var answer = false;

          for (var i = 0; i < medlist.length; i++) {
            // The (old) "drugname" access
            // if (is_a_statin(medlist[i].drugname.value))

            // The new property access
            // Note how the names come directly from the datamodel
            // and no ".value" required anymore!
            if (is_a_statin(medlist[i].drugName.dcterms__title)) { answer = true; }
          }

          document.getElementById("TheAnswer").innerHTML = answer ? "Yes." : "No.";

        });

          var is_a_statin = function(drug) {
            if (drug.match(/statin/i)) return true;
            if (drug.match(/Advicor/i)) return true;
            if (drug.match(/Altoprev/i)) return true;
            if (drug.match(/Caduet/i)) return true;
            if (drug.match(/Crestor/i)) return true;
            if (drug.match(/Lescol/i)) return true;
            if (drug.match(/Lipitor/i)) return true;
            if (drug.match(/Mevacor/i)) return true;
            if (drug.match(/Pravachol/i)) return true;
            if (drug.match(/Simcor/i)) return true;
            if (drug.match(/Vytorin/i)) return true;
            if (drug.match(/Zocor/i)) return true;
            return false;
          }
      });
    </script>
  </body>
</html>
{% endhighlight %}

[Got Statins?]: /howto/got_statins


# Learning More

SMART's JSON-LD API gives you as a web developer an natural, familiar,
and interactively discoverable interface to SMART patient data. You can
start using this API in your apps today. For examples of this API in use
see the code (in `main.js`) for the SMART [Diabetes Monograph app][].

[Diabetes Monograph app]: https://github.com/chb/smart_sample_apps/tree/master/static/framework/dm_monograph/js/main.js

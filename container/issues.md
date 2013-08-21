---
layout: default
title: SMART Developers Documentation
---

# Topics of Interest to Container Developers

## Translating between coding systems

Chances are that your medical data is already encoded in one of the widely available coding
standards used in the medical community. When exposing your data through the SMART API,
you will have to provide data about the patient using the coding systems defined by
SMART (such as SNOMED-CT, RXNORM, LOINC, etc). Thus, you will need to map your local
data codes into the SMART defined coding systems.

Unfortunately, the problem of generating accurate translations between coding
systems is an inexact science. Due to differences between the terminology terms,
it is often times not possible to derive a complete one-to-one map between
two systems to preclude loss of meaning as result of translation. A good
practice when generating SMART RDF with translated codes is to include
provenance information. Here is an example that specifies the provenance for 
a lab result translation from a local labcode to LOINC:

{% highlight xml %}
<sp:labName>
    <sp:CodedValue>
        <sp:code rdf:resource="http://loinc.org/codes/2951-2"/>
        <dcterms:title>Serum sodium</dcterms:title>
        <sp:codeProvenance>
            <sp:CodeProvenance>
                <sp:sourceCode rdf:resource="http://local-emr/labcodes/01234" />
                <dcterms:title>Random blood sodium level</dcterms:title>
                <sp:translationFidelity rdf:resource="http://smartplatforms.org/terms/code/fidelity#automated" />
            </sp:CodeProvenance>
        </sp:codeProvenance>
    </sp:CodedValue>
</sp:labName>
{% endhighlight %}

For translating from one system to another, we highly recommend reusing commonly
available maps. For example, the US National Library of Medicine provides maps for 
translation between ICD-9-CM and SNOMED-CT 
([http://www.nlm.nih.gov/research/umls/mapping_projects/icd9cmv3_to_snomedct.html](http://www.nlm.nih.gov/research/umls/mapping_projects/icd9cmv3_to_snomedct.html),
[http://www.nlm.nih.gov/research/umls/mapping_projects/icd9cm_to_snomedct.html](http://www.nlm.nih.gov/research/umls/mapping_projects/icd9cm_to_snomedct.html)).

## RDF vs JSON

(add discussion points here)

## Partial implementations

Implementing the complete SMART specification on top of your medical records system
will allow you and your system's users to run the full range of standard SMART medical apps
available on the market. However, a complete implementation may turn out to be a large scale project.
Some times the objective of a SMART enablement project is to enable running specific
applications on a medical records system. Under such a scenario, you may want to
consider a partial implementation of the SMART standard following the least common
denominator principle. SMART provides for a discovery mechanism that can be used by SMART
apps to learn about the API calls supported by a container by requesting the container
manifest through the `/manifest` REST path. For example, the public sandbox of the SMART
Platforms project exposes its manifest on the following URL:
[http://sandbox-api.smartplatforms.org/manifest](http://sandbox-api.smartplatforms.org/manifest)

Even if your end goal is complete SMART support, it may still be a good development
strategy to start small and implement a few maningful basic API calls and testing 
your container with some basic apps that rely on them. Since a large majority of the SMART
apps our there use the SMART Connect interface, it would make sense to focus on implementing
this interface before tackling the SMART REST interface which requires, amongst the others,
OAuth support. Starting with the Demographics data model and API a developer may wish to
consider implementing the Medications, Problems, or VitalSigns interfaces.

## Reusing portions of the SMART Reference Container

## Extending the SMART API and data models

## Implementing write capabilities
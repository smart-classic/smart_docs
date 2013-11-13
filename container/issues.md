---
layout: container
title: SMART - Container Development Issues
---

## Container Development Issues

### Translating Between Coding Systems

Chances are that your medical data is already encoded in one of the widely
available coding standards used in the medical community. When exposing your
data through the SMART API, you will have to provide data about the patient
using the coding systems defined by SMART (such as SNOMED-CT, RXNORM, LOINC,
etc). Thus, you will need to map your local data codes into the SMART defined
coding systems.

Unfortunately, the problem of generating accurate translations between coding
systems is an inexact science. Due to differences between the terminology
terms, it is often times not possible to derive a complete one-to-one map
between two systems to preclude loss of meaning as result of translation. A
good practice when generating SMART RDF with translated codes is to include
provenance information. Here is an example that specifies the provenance for a
lab result translation from a local labcode to LOINC:

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

For translating from one system to another, we highly recommend reusing
commonly available maps. For example, the US National Library of Medicine
provides maps for translation between ICD-9-CM and SNOMED-CT
([http://www.nlm.nih.gov/research/umls/mapping_projects/icd9cmv3_to_snomedct.html](http://www.nlm.nih.gov/research/umls/mapping_projects/icd9cmv3_to_snomedct.html),
[http://www.nlm.nih.gov/research/umls/mapping_projects/icd9cm_to_snomedct.html](http://www.nlm.nih.gov/research/umls/mapping_projects/icd9cm_to_snomedct.html)).

### RDF vs JSON

RDF is the internal format in which SMART structures the patient records data.
A SMART server instance responds to REST API calls for medical data with RDF
serialized as RDF-XML. The XML data received from SMART is typically non-deterministic
in nature (i.e. it can change with each request on the same data element, even
when the underlying patient data remains constant). This is because RDF-XML is 
a projection (flat representation) of a the RDF graph structure expressing the 
patient record. In the SMART reference container the patient RDF graph is stored in a
specialized triple store engine. Because the serialization of the RDF as RDF-XML
is perfomed at the triple store level, it is the result of the store's graph walk
algorithm which favors speed over predictive order of results. Thus, every time
the RDF-XML is produced by the server, it will be different from the preceeding runs.

Developers used to working with XML may be tempted to view the RDF-XML as a typical
XML payload and apply pattern recognition strategies (XPath, XQuery, XSLT, etc) to
extract data from it. Unfortunately, the non-deterministic nature of this XML payload
breaks the assumptions of these approaches rendering them useless. The correct way to
work with RDF-XML is to use an RDF parser which reconstructs the patient graph in a data
structure that can be querried with SPARQL, the query language for RDF graphs. This approach
requires a non-cursory level of understnading of RDF that is not common amongst developers.

As an alternative to RDF SMART when using the SMART Connect JavaScript client, the SMART
app developers have the option of fetching the patient data in JSON fromat which could
be a more familiar structure to many. One advantage of JSON over RDF is that the JSON
representation of the patient record is predictable (i.e. deterministic). Also,
by using the JSON structure available in the SMART Connect client response objects,
there is no need to learn SPARQL. The disadvantage over RDF though is that the JSON
object is not as well adapted to use with logic reasoners as the RDF graph would be
and also not as flexible to extend. This said, developers should try both approaches
and pick the one which works better for their needs and style.

### Partial Implementations

Implementing the complete SMART specification on top of your medical records
system will allow you and your system's users to run the full range of standard
SMART medical apps available on the market. However, a complete implementation
may turn out to be a large scale project.  Some times the objective of a SMART
enablement project is to enable running specific applications on a medical
records system. Under such a scenario, you may want to consider a partial
implementation of the SMART standard following the least common denominator
principle. SMART provides for a discovery mechanism that can be used by SMART
apps to learn about the API calls supported by a container by requesting the
container manifest through the `/manifest` REST path. For example, the public
sandbox of the SMART Platforms project exposes its manifest on the following
URL:
[http://sandbox-api.smartplatforms.org/manifest](http://sandbox-api.smartplatforms.org/manifest)

Even if your end goal is complete SMART support, it may still be a good
development strategy to start small and implement a few maningful basic API
calls and testing your container with some basic apps that rely on them. Since
a large majority of the SMART apps our there use the SMART Connect interface,
it would make sense to focus on implementing this interface before tackling the
SMART REST interface which requires, amongst the others, OAuth support.
Starting with the Demographics data model and API a developer may wish to
consider implementing the Medications, Problems, or VitalSigns interfaces.

### Reusing Portions of the SMART Reference Container

As discussed in the [reference container](reference-container.html) section,
the SMART Platforms team maintains an open-source complete medical system that
implements the SMART specification.  The reference container is available under
Apache 2 open source license and can serve as a base for rapid SMART container
implementations. One of the implementation strategies outlined in the [roamap
for container developers](roadmap.html) is replacing the reference contianer's
data source and user authentication subsystems with an adapter to your medical
data system. The downside of reusing the reference container code is that it
has not been tested in highly scalable environments and will introduce
dependencies on Python/Django based code components.

### Extending the SMART API and Data Models

While not a common practice, your SMART container implementation can extended
the SMART specification with new API calls and data models that support the
needs of your specific community.  Apps written to take advantage of these
non-standard calls that need to run on a standard SMART container will need to
degrade gracefully in the absence of the extended API calls.

## Implementing Write Capabilities

With the exception of the Clinical Notes, Preferences, and Scratchpad APIs, the
SMART standard does not provide for write functionality in the container.
Therefore the majority of the SMART apps presently available assume read-only
interactions with the container. However, a container may provide write
capabilities.

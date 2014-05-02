---
layout: smart_on_fhir
title: SMART on FHIR
---

<h1>Tech Stack for Health Apps</h1>

SMART on FHIR is an open platform to integrate health apps with EHRs, 
portals, and other health systems. You get...

<h3 id="clean"> Clean, structured data:  <b>FHIR</b></h3>

Your app gets an easy-to-use, resource-oriented REST API for structured
clinical data.  Fetching patient demographics is as easy as:

```
$ curl https://open-api.fhir.me/Patient/1032702 -H 'Accept: application/json'
{
  "resourceType": "Patient",
  "identifier": [{
      "use": "usual",
      "label": "SMART Hospiptal MRN",
      "system": "http://smart-hospital/mrn",
      "value": "1032702"
    }],
  "name": [{
      "use": "official",
      "family": [ "Shaw" ],
      "given": [ "Amy", "V." ]
    }], 
   ...
}
```

<h3 id="oauth">Permissions:  <b>OAuth2</b></h3>

Your app will get a "launch request" notification from the EHR. This
notification includes a context identifier that you'll use to create an OAuth
authorization request. Just define a `scope` that identifies the access you
need. For example, if your app needs to access patient demographics,
prescriptions, and lab results you'll request a scope like: 

```
{
  "context": "1234",
  "patientData": {
    "Observation": ["read"],
    "MedicationPrescription": ["read"],
    "Patient": ["read"] 
  }
}
```

After engaging in the "OAuth dance,"  you'll have an access token with the
permissions you need -- including access to clinical data and context such as:

 * which EHR user launched the app
 * which patient is in-context in the EHR (optional)
 * which encounter is in-context in the EHR (optional)
 * what location is the EHR user working from (optional)



<h3 id="openid">Sign-in:  <b>OpenID Connect</b></h3>

If your app needs to authenticate the EHR end-user, OpenID Connect is there to
help. Just ask for one additional scope (`openid`) when you request
authorization, and you'll have access to a `UserInfo` endpoint that exposes
structure claims about the user, including name and NPI.

<h3 id="html">UI integration:  <b>HTML5</b></h3>

Need to hook your app into an existing EHR user interface? SMART on FHIR allows
web apps to run inside browser widgets or inline frames, so users can interact
without leaving the EHR environment. Of course, native and mobile apps are
supported too -- so you can choose the level of integration that makes sense
for you.

{% raw %}
<example>
**An example here**
<pre>
pre
</pre>
</example>
{% endraw %}

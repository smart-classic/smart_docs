---
title: What is SMART?
layout: default
---

## What is SMART?

SMART defines a open source platform based on web standards for building
substutiable apps on medical data systems such as electronic medical records,
personal health records, clinical data systems and health information
exchanges. SMART is designed to help solve the problems in both exposing
medical data to apps and the creation of innovative, substutiable apps for
these systems.

The SMART platform defines four main components:

1. A developer-friendly data model covering the most commonly used medical data
elements such as problems, medications, labs, vital signs, encounters, and
fulfillments. The data is meaningfully structured with references to relevant
coding systems and related data is linked. For example, a given fulfillment
references the related medicaion which references a specifc RxNorm code.

2. A easy-to-use REST API to access the data

3. A simple set of standards based on widely used, off-the-shelf protocols for
app registration, authenticaion, and authorization

4. A set of software development tools including native client libraries for
Javascript, Python, iOS, and Java and a _reference EMR_ for testing

In addition to the above, the SMART platforms team provides documentation and
support to app and container developers including a cloud hosted reference EMR
filled with sample patient data.


### The SMART Container

A medical data system that exposes the SMART API is a _SMART container_.
Several existing systems have been "SMART enabled" including the OpenVistA
electronic medical record, the Indivo personal healh record, the i2b2 clinical
data system, and the Mirth Results health information exchange system. More
systems both academic and commercial are planning to become SMART enabled in
the near future.

See our [FAQ](/faq.html) for answers to further questions.

<!---
How Do I Write Medical Apps With SMART?
How Do I "SMART Enable" My System?
Who is Using SMART?
Is SMART a "Standard"?
--->

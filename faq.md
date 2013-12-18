---
layout: resources
title: SMART - Frequently Asked Questions
---

# Frequently Asked Questions about SMART

## What is SMART?

SMART is a specification of a open source platform based on web standards for
building substitutable apps on medical data systems such as electronic health
records, personal health records, clinical data systems and health
information exchanges. The SMART specification is designed to help solve the
problems in both exposing medical data to apps and the creation of innovative
substitutable apps for these systems.

The SMART platform defines four main components:

1. A developer-friendly data model covering the most commonly used medical data
   elements such as problems, medications, labs, vital signs, encounters, and
   fulfillments. The data is meaningfully structured with references to
   relevant coding systems and related data is linked. For example, a given
   fulfillment references the related medicaion which references a specifc
   RxNorm code.

2. A easy-to-use REST API to access the data models above

3. A simple set of specifications based on widely used, off-the-shelf protocols
   for app registration, authenticaion, and authorization

4. A set of software development tools and documentation including native
   client libraries for Javascript, Python, iOS, and Java (the SMART Framework)
   and a _Reference EMR_ for testing referred to as the "SMART Reference
   Container".


## What is a SMART Container?

The concrete implementations of the SMART Platform" either using the provided
SMART Framework or built into an EHR system are called SMART Containers.

For example, our cloud-hosted reference EMR filled with sample patient data for
convenient testing of SMART apps is our implementation of the SMART platform
built with the SMART Framework and called the SMART Reference Container.

Several existing systems have been "SMART enabled" including the OpenVistA
electronic medical record, the Indivo personal healh record, the i2b2 clinical
data system, and the Mirth Results health information exchange system. More
systems both academic and commercial are planning to become SMART enabled in
the near future.


## What is the SMART Reference Container?

The SMART Reference Container is our reference implementation of SMART. It is a
self-contained sample EHR that fully implements the SMART specification. The
reference container is useful for development and testing of SMART applications
whithout the need to have access to a SMART-enabled hospital EHR. It also is
intended to serve as an example of a SMART container that can be examined by
container developers who are in the process of SMART-enabling their EHR.


## How do I "install" SMART in my EHR?

Since SMART is a specification of a platform for medical apps and not a piece
of software it can't be "installed" into a system. However, to aid in the
adoption of the SMART platform, we've created the SMART Framework, which is a
set of software libraries and tools to help you SMART enable your system.

To get started, see our [container developers guide](container/).


## Is SMART a "standard"?

SMART is currently not overseen by a formal standards body.


## Can I write data into my EHR through SMART?

As of SMART v0.6, the framework supports very limited write capabilities.
Specifically, a SMART app can write clinical notes and store its preferences
and annotations of a patient record as unstructured data. Most of the API calls
in SMART are read-only.


## How Do I Write Medical Apps With SMART?

Getting started creating amazing apps is easy! Start with our [app developer's
getting started guide](/guide/about.html).


## Who is Using SMART?

See our list of [SMART containers](/container/examples.html)




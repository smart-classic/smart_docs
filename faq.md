---
layout: default
title: SMART Developers Documentation
---

#Frequently Asked Questions

##How do I install SMART in my electronic health records system (EHR)?

We get this one a lot...

SMART is a framework that supports the development and deployment of
medical applications on top of EHRs. It compromises a set of standards that define how an EHR
can launch medical apps, how the apps authenticate with the EHR, the format of data that
the apps receive from the EHR, and the API calls that the EHR should expose to the apps. 
Therefore, SMART is not a software application that can be installed in an environment in and
of itself.

You can run SMART apps on your EHR, if the EHR that you have is SMART-enabled or you have a
SMART-enabled product that can connect to your EHR and retrieve data from it. If you have
an EHR that you would like to SMART-enable, please check out our
[container developers guide](container/).

##What is the SMART reference container?

The SMART reference container is our reference implementation of SMART. It is a self-contained
sample EHR that fully implements the SMART specification. The reference container is useful
for development and testing of SMART applications whithout the need to have access to a
SMART-enabled hospital EHR. It also is intended to serve as an example of a SMART container
that can be examined by container developers who are in the process of SMART-enabling their
EHR.

##Can I write data into my EHR through SMART?

As of SMART 0.6, the framework supports very limited write capabilities. Specifically,
a SMART app can write clinical notes and store its preferences and annotations of a patient
record as unstructured data. Most of the API calls in SMART are read-only.
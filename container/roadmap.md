---
layout: container
title: SMART - Roadmap for Container Development
---

## Roadmap for Container Development

### Overview

In practice, there are a couple alternative approaches to the task of
SMART-enabling an existing medical system. These fall into the categories of
reusing the SMART reference container as a sidecar for SMART enablement and
building a tightly integrated container grounds-up. The following is a
discussion of the costs and benefits of each approach. We try to outline the
main steps that you will need to follow in order to successfully build your
SMART container following either approach.

### SMART Reference Container Reuse

The fastest way to get a complete SMART implementation is to deploy the SMART
Reference Container and replace its data layer and authentication modules with
implementations specific to the medical records system that will be providing
the data. The downside of this approach is that it locks the developer into a
depenency upon an external piece of code that is not necessarily optimal for
the needs of the particular implementation nor scalable enough. In addition,
the SMART Reference Container is built upon Python and Django, which may be an
administrative burden to the deployment site, especially if the medical system
is based on another technology. Finally, the reference container adds
processing overhead which can be avoided with a tightly-coupled native
implementation of SMART.

The SMART reference container UI server provides a sample web-based UI for
running SMART apps on top of medical records. However, it most likely is less
than ideal for the needs of most containers necessitating a degree of
customization or complete replacement.

(TODO: add description of the steps for securing the reference container, enabling
proxy mode, and testing the installation)

### Implementing a SMART Container from Scratch

Arguably the best way to SMART-enable your system is through a grounds-up
implementation specific to your medical records system. Such an implementation
has the potential of offering the most efficient robust SMART container yet
will require more effort than the previously described approach. A good
starting point for this approach is to implement the SMART Connect interface
first (or a subset of it) based on our [Sample Container Tutorial](#). (TODO
add details here)

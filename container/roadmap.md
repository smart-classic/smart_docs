---
layout: container
title: SMART - Roadmap for Container Development
---

## Roadmap for Container Development

There are a few possible approaches to the task of SMART-enabling an existing
medical system. The two main approaches are (1) reusing the SMART reference
container as a "sidecar" to your current system and (2) building a tightly
integrated container from the ground-up. We discuss the costs and benefits of
each approach below. Additionally, We outline the main steps that you will
need to take to successfully build your SMART container with either approach.


### Reusing the SMART Reference Container

The fastest way to a SMART implementation is to deploy the SMART Reference
Container replacing its data layer and authentication modules with new modules
that integrate with your existing systems. The downside of this approach is
that it locks your developers into a depenency upon an external piece of code
that is not necessarily optimal for your particular needs. In addition, the
SMART Reference Container is built upon Python and Django, which may be an
administrative burden to the deployment site, especially if the medical system
is based on another technology. Finally, the reference container adds
processing overhead which can be avoided with a tightly-coupled native
implementation of SMART.

The SMART reference container UI server provides a sample web-based UI for
running SMART apps on top of medical records. However, it most likely is less
than ideal for the needs of most containers necessitating a degree of
customization or complete replacement.

Should you decide to use the SMART reference container in a production environment
to store protected patient data, you should be careful about securing your installation.
Besides following good security practices for your server, you should also at
the very minimum:

   * change the default secrets on the SMART apps installed on the machine
(or remove them by resetting the sever)
   * disable the unsupervised account creation page (or password protect
it)
   * enforce SSL connections over HTTP in the Apache config
   * if you are planning on using OpenRDF based on the SMART reference
container installation guide, make sure that you disable remote access to
Tomcat as described in the installation guide

If you need to replace the data layer of the reference container with your own,
perhaps the easiest approach is to set the container in proxy mode by editing
`settings.py` in the smart_server (https://github.com/chb/smart_server/blob/master/settings.py.default).
In proxy mode, the reference container will issue REST calls for patient data directly to
the REST base that you specify instead of querying its internal triplestore.


### Implementing a SMART Container from Scratch

The best way to SMART-enable your system may be through a ground-up
implementation specificly tailored to your medical records system. Such an
implementation has the potential of offering the most efficient and robust
SMART container for you yet will require more effort than the first approach.
A good starting point for this approach is to first implement the SMART Connect
interface based on our [Sample Container Tutorial](./tutorial.html).

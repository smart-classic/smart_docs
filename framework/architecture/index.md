---
layout: default
title: SMART Developers Documentation
---

#Architecture

# Vocabulary and basics

The first component of the SMART universe is the ecosystem of SMART apps created
by various software developers eager to bring solutions in the hands of
clinicians and patients. The apps could include a medication manager, a 
diabetes evaluation suite, or perhaps a lab results visualizer. These
meaningful apps could be distributed via an app store.

Then we have the containers which play the role of data providers 
in the SMART world. The containers could be personally controlled
health records systems, electronic medical records systems, health
data exchanges, or other providers. Either way a container is
responsible for exposing the SMART API to the apps and providing
a context in which the apps could run.

Finally, we have the interface which enables the apps and containers
to talk to each other – the SMART application programming interface (or API).
The API is what keeps the apps and the containers decoupled from each
other allowing the users to mix and match. 

Also, the API enables the substitutability of the SMART apps and
containers. From the perspective of an app the containers are
substitutable, because they all expose the same interface and
the app can run on any one of them. Also from the perspective
of the container, the apps are substitutable. The container
administrator is free to pick the apps that he needs. And when
a better app comes along, he can replace the existing app with
the new one. 

In order to keep things simple, an app runs against one
container at a time. The container, however, is free to
connect to multiple data sources and aggregate data as needed.

## APIs

At the bottom of the diagram we have the frond end of the container
and the smart application within a web browser window. The container
and the app might also have back end server components. For the
container the back end component might be an EMR system housing
a large collection of medical records. The app could have a back
end that helps with elaborate visualizations, data mashing, or
other complex computations. 

On front end components use an interface called SMART Connect
to communicate with each other right inside the browser environment.
Using it the app can get patient context from the container and
execute API calls. The back end components can also talk to each
other. And for that they use an interface called SMART REST.
Should an app choose to use the SMART REST interface, it simply
has to obtain an authentication token from the container using
SMART Connect, and pass it to the back end component, which can
then use it to issue SMART REST calls to the container’s back end.

## Architectural Components

Now, let’s look at the elements that an app needs in order to provide
a meaningful service to the end user. First, the app needs a flexible,
standards-based UI that enables the user to interact with it. Next,
the app needs to have an authentication mechanism with the container
to establish thrust. And last but not least, the app needs data in
order to work with. The data includes patient and provide context
information, as well as medical record elements such as medications
and lab results. We will look at each one of these components in more details.

(insert diagram) This diagram illustrates the container’s UI component in a browser window.
The white portion of the screen is the UI that the container provides,
which allow the user for instance to choose a patient and launch various
SMART applications on his data. The main portion of the screen real estate
is taken by the SMART app. The app is launched by the container in an IFRAME.
An IFRAME is an in-browser mechanism that enables multiple web pages to open up
on the same screen. When launched the app establishes a channel to the container
using the SMART connect JavaScript library. It can then issue SMART API calls such
as GET MEDICATINS in order to obtain data from the container. Finally, the app
displays the data to the user and allows him to interact with it.

The next architectural piece is the authentication mechanism. Different EMR systems
have their own authentication schemas. In order to keep the app agnostic to them,
it is the container’s responsibility to provide a standard way for establishing
trust. And for that SMART uses oAuth, which is an open web standard for authentication.
Thus the app does not have to deal with the underlying system’s  permissions
schema. All it needs is to speak OAuth. The container uses his internal logic
to decide what the app can see and what is forbidden.

The last component of the architecture is the medical data. And for that SMAR
takes what we call an “80/20” approach.  What this means is that we try to
pick the 20% of the fields out there that represent 80% of the data about
the patients. This selectivity of SMART is one thing that makes writing SMART
apps relatively easy. Also, SMART uses consistent best-of-the-breed coding
systems for representing medical facts within the SMART data models. For
example for medications we use RXNORM, for problems we use SNOMED, and labs
are based on LOINC. The SMART data payloads are expressed in RDF and are extensible.

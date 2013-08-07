---
layout: default
title: SMART Developers Documentation
---

# Setting up your Environment

A SMART app is a web application that is loaded in an IFRAME hosted by a SMART
container. That means you need to (a) write a web app, and (b) connect it to a
SMART container.

You can choose any toolkit you want to write a web app: Java Spring, Ruby on
Rails, Python/Django, etc. For the purposes of this documentation, we've chosen
webpy, a very simple, minimalist Python web framework, which helps us show you
the important SMART-related code more quickly. Also, if you want to get going
quickly with the more advanced app features, you probably want to stick with
Java or Python for now, as those are the two programming languages in which
we've built client libraries. That said, if you're comfortable with OAuth and
REST, you can use another programming language without fear.

We also provide you with a SMART EMR hosted at `sandbox.smartplatforms.org`. We
call it the SMART Reference EMR, and we've loaded it with 50 patient records on
which you can try out your app. To get going, you'll need to:

<ol>
  <li>Navigate to the [developers sandbox](http://sandbox.smartplatforms.org/login")</li>
  <li>If you haven't done so already, create an account, otherwise just log back in </li>
  <li>Select a patient </li>
  <li>Run the app called &quot;My App&quot; </li>
</ol>

This will open a SMART app iframe pointing to `localhost:8000`, which is where
your app should be running. If you need an app with a different hostname (say,
my_internal_server.net), just e-mail joshua dot mandel at childrens.harvard.edu
with a manifest file and we'll set you up!
---
layout: guide
title: SMART Developers Documentation
---

## Setting up your Environment

A SMART app is a web application that is loaded into an &lt;IFRAME&gt; hosted
by a SMART container. That means you need to (1) write a web app, and (2)
connect it to a SMART container.

You can choose any toolkit you want to write your web app: Java Spring, Ruby
on Rails, Python/Django, etc. For this tutorial, we've chosen
[webpy](http://webpy.org/), a minimalist Python web framework. Using this
simple micro-framework will help you see and understand the important
SMART-related code more quickly without a lot of framework code getting in
the way.

Also, if you want to get started with more advanced SMART features, you will
want to use Python or Java since client libraries are currently available for
those languages. (Note that the Java client may not as up-to-date as the
Python client). That said, if you're comfortable with OAuth and REST, you can
comfortably use your preferred programming language.

We also provide you with the hosted SMART Reference EMR at
<sandbox.smartplatforms.org>. It's loaded with 50 patient records on which to
test your apps.

The process to run your app on the Reference EMR is:

<ol>
  <li>Go to the [developers sandbox](http://sandbox.smartplatforms.org/login)</li>
  <li>Create an account or log in </li>
  <li>Select a patient </li>
  <li>Run the app called &quot;My App&quot; </li>
</ol>

That will open a SMART app &lt;IFRAME&gt; pointing to your own local system
e.g. `localhost:8000`, where your app will then be listening for connections.

Next: [the quickstart example](quickstart.html)

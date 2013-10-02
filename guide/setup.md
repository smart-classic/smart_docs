---
layout: default
title: SMART Developers Documentation
---

## Setting up your Environment

A SMART app is a web application that is loaded into an &lt;IFRAME&gt; hosted
by a SMART container. That means you need to (1) write a web app, and (2)
connect it to a SMART container.

You can choose any toolkit you want to write your web app: Java Spring, Ruby on
Rails, Python/Django, etc. For this tutorial, we've chosen webpy, a minimalist
Python web framework. This simple framework will help you see and understand
the important SMART-related code more quickly.

Also, if you want to get started with more advanced SMART features, you will
want to use Python or Java since client libraries are currently available for
those languages. That said, if you're comfortable with OAuth and REST, you can
comfortably use your preferred programming language.

We also provide you with the hosted SMART Reference EMR at
<sandbox.smartplatforms.org>. It's loaded with 50 patient records to test your
apps on.

To get going, you'll need to:

<ol>
  <li>Go to the [developers sandbox](http://sandbox.smartplatforms.org/login")</li>
  <li>If you haven't done so already, create an account, otherwise log in </li>
  <li>Select a patient </li>
  <li>Run the app called &quot;My App&quot; </li>
</ol>

This will open a SMART app iframe pointing to `localhost:8000`, where
your app will be listening for connections.

Next: [the quickstart example](quickstart.html)

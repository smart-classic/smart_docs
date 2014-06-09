---
layout: framework
title: SMART - Using $.deferred with SMART Connect
---

## Using the jQuery Deferred Object with SMART Connect

When using the SMART Javascript API you frequently want to make multiple
requests for data (for instance to get both demographics and labs for a lab
viewer app) and then do something with the result of both calls. In pure
Javascript, the typical pattern is for a deeply nested and serial chain of
callback functions. Using the jQuery Deferred objects you can easily make
faster parallel requests in a well organized way without confusing and messy
nested callbacks.

The [Deferred Object](http://api.jquery.com/category/deferred-object/) is
utility object in jQuery to define sets of callbacks that can signal a observer
function allowing the observer to conditionally execute code based on differing
success or failures states.

What this means in practice is that you can now easily make concurrent,
asynchronous function calls to the SMART Connect API and have those functions
signal an observer function at the moment when they are both complete along
with simple error handling in case of failures. This is useful for increasing
the performance of your app with parallel ajax calls and, once you are familiar
with the pattern, to avoid messy code structures like deeply nested callbacks.

Using this pattern is similar to attaching multiple callback functions to
[jQuery.ajax's](http://api.jquery.com/jQuery.ajax/) `.success`, `.error`, and
`.complete` handlers, in fact, those handlers use Deferred Object under the
hood.


### Mapping jQuery.ajax handlers to Deferred Object handlers

- `.complete()` is analogous to `.then() or .always()`
- `.success()` is analogous to `.done()`
- `.error()` is analogous to `.fail()`


### A Real-World Example

[The Cardiac Risk Visualiztion
App](https://github.com/smart-platforms/smart_sample_apps/blob/master/static/framework/cardi
o_risk_viz/load_data.js) requires both demographics (gender and age) and also
lab results (hsCRP, cholesterol, and HDL values) to compute a risk score. This
requires two calls to the SMART Connect API:
[get_demographcis](http://wiki.chip.org/smart-project/index.php/Developers_Docum
entation:_SMART_App_Javascript_Libraries#SMART.get_demographics) and
[get_lab_results](http://wiki.chip.org/smart-project/index.php/Developers_Docume
ntation:_SMART_App_Javascript_Libraries#SMART.get_lab_results).

In the code below each of these calls is wrapped in a function that is
registered with $.when. Once all the registered functions signal they have now
successfully completed `(by calling .resolve())` or have failed `(by calling
.reject())` on their Deferred object the function attached to the `.then()`
handler is executed. Which in this example draws the full visualization being
safe in the knowledge that all the required data is available.

One detail to note is that both functions return the Deferred's promise object
to the observer. A promise object is the read-only object that is used by the
observer function to query the current state of the function and therefore is
the required return value of the callbacks.


### Error Handling

The failure case is not handled in the code below, but a `.fail()` handler
could be added after the `.then()` handler. In that case, if the attached
functions would signal a failure state by calling `.reject()` on their Deferred
object, the code attached to the `.fail()` handler would be executed.


### The Code

{% highlight javascript %}
    // note: code simplified
    var get_demographics = function() {
          // create an instance of the jQuery Deferred object in the 
          // initial "pending" state
          var dfd = $.Deferred();

          // do the SMART Connect Call and execute the associated callback
          SMART.get_demographics().success(function(demos) {

            // extend the global object "p" with the returned data
            $.extend(p, demos.graph.prefix('foaf', 'http://xmlns.com/foaf/0.1/')
                             .prefix('v', 'http://www.w3.org/2006/vcard/ns#')
                             .prefix('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
                             .where('?r v:n ?n')
                             .where('?n rdf:type v:Name')
                             .where('?n v:given-name ?givenName')
                             .where('?n v:family-name ?familyName')
                             .where('?r foaf:gender ?gender')
                             .where('?r v:bday ?birthday')
                             .get(0))

            // signal that this Deferred object is now "resolved"
            dfd.resolve();
          });

          // return a Promise object used by the observer 
          return dfd.promise();
      };

      var get_labs = function() {
          var dfd = $.Deferred();

          SMART.get_lab_results().success(function(labs){
              labs.graph.where("?l rdf:type sp:LabResult")
                  .where("?l sp:labName ?ln")
                  .where("?ln sp:code <http://loinc.org/codes/30522-7>")
                  .where("?l sp:quantitativeResult ?qr") // predicate
                  .where("?qr rdf:type sp:QuantitativeResult") // type
                  .where("?qr sp:valueAndUnit ?vu")
                  .where("?vu sp:value ?v")
                  .each(function(){ p.hsCRP.value = Number(this.v.value); })

              dfd.resolve();
          });

          return dfd.promise();
      }

      ...

      SMART.ready(function() {
          // when the Promise objects of these two asynchronous functions
          // report that they both are in either the "resolved" or "rejected"
          // state, execute the callback function to draw the visualization
          $.when(get_demographics(), get_labs()).then(function() {
            draw_visualization();
          });
      });

{% endhighlight  %}


### A Shorter Syntax

The get_demographics() and get_labs() functions above can also be written using
a more compact (but equivalent) syntax:

{% highlight javascript %}
 var get_demographics = function() {
  // using the shorter $.Deferred(fn).promise() signature
  return $.Deferred(function(dfd){
    SMART.get_demographics().success(function(demos) {
    $.extend(p, demos.graph.prefix('foaf', 'http://xmlns.com/foaf/0.1/')
                     .prefix('v', 'http://www.w3.org/2006/vcard/ns#')
                     .prefix('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
                     .where('?r v:n ?n')
                     .where('?n rdf:type v:Name')
                     .where('?n v:given-name ?givenName')
                     .where('?n v:family-name ?familyName')
                     .where('?r foaf:gender ?gender')
                     .where('?r v:bday ?birthday')
                     .get(0))
      dfd.resolve();
    });
  }).promise();
};
{% endhighlight  %}


### Further Reading

* [Deferred Object](http://api.jquery.com/category/deferred-object/) in jQuery's API docs
* [Eric Hynds' article](http://www.erichynds.com/jquery/using-deferreds-in-jquery/) for a further explanation and examples

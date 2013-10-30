---
layout: framework
title: Authentication and Authorization in SMART with OAuth
---

# Authentication and Authorization in SMART with OAuth

## Prerequisites

### App ###

Any SMART app needs to be registered on the SMART container it wants to
interact with. The app chooses an `app-id` (usually in email format) and the
server assigns a `consumer_key` (usually the same as the app-id) and a
`consumer_secret`.

In order to launch the app, it needs to provide an `index` URL in the manifest.
Opening this URL, with appended parameters `record_id` and `api_base`
(explained below), provides your app with all the information it needs to get
started.


### Server ###

Every SMART server exposes these URLs:

- `/apps/{app-id}/launch`
  The launch page for any app with the goal of returning a record-id to the app.
  This page usually displays a list of records after the user logs in, selecting
  a record loads the app's `index` URL.

- `/oauth/request_token`
  Returns a request token if the app's consumer-key and -secret are valid

- `/oauth/authorize`
  Authorizes the request token if the user agrees that the app may access the
  data for this record. Returns a verifier to the app's callback url.

- `/oauth/access_token`
  Returns an access token if the verifier is valid


## Authentication Flow

### 1. Launching an App ###

SMART access tokens are scoped to a specific record, thus an app must supply a
record-id when requesting a token. An app however has no permissions to get a
list of record-ids, which is why the container launches your app's `index` URL
with appended `record_id` and `api_base` parameters:

    http://www.myapp.com/go.py?record_id={record-id}&api_base={api-base}

The app can now extract the record-id and the REST server URL. The latter can
be used to retrieve the OAuth endpoints by requesting the manifest from the
server:

    GET {api-base}/manifest

A JSON file is returned which contains the URLs we're interested in:

    {
        "version": "0.4", 
        …
        "launch_urls" : {
            "request_token_url": "http://localhost:7000/oauth/request_token", 
            "authorize_token_url": "http://localhost:7001/oauth/authorize", 
            "exchange_token_url": "http://localhost:7000/oauth/access_token"
        }
    }


#### Selecting a Record ####

If your app is not being launched from a container UI and thus does not have a
record-id, your app can load a launch page located at `/apps/{app-id}/launch`
in a browser (or embedded web-view). Usually, the server displays a list of
available records at that URL after the user has logged in.


### 2. Requesting a Request Token ###

Armed with the record-id and the server URLs, the app can now start the OAuth
dance and request a request token by issuing a **POST** request to the
`request_token_url`:

    POST /oauth/request_token

The standard OAuth parameters, with the callback url (`oauth_callback`) set to
`oob` since it is defined in the app manifest, should go into the
**Authorization** header. The record-id must be provided as an additional
header parameter called `smart_record_id`.

    oauth_callback=oob
    oauth_consumer_key={consumer-key}
    oauth_nonce={oauth:nonce}
    oauth_signature_method=HMAC-SHA1
    oauth_timestamp={oauth:timestamp}
    oauth_version=1.0
    oauth_signature={oauth:signature}
    smart_record_id={record-id}

If the call was successful, an HTTP status code `200` is returned and the
response body will contain the token:

    oauth_token={req-token}&
    oauth_token_secret={req-secret}&
    oauth_callback_confirmed=true

> **Note:** `oauth_callback_confirmed` is currently NOT returned from our
> reference container, but according to [section 2.1](http://tools.ietf.org/html/rfc5849#section-2.1)
> it must be present.

Otherwise, an HTTP `403` status code is returned.


### 3. Authorizing the Token ###

The request token needs to be authorized by the user. To do so the app loads
the ` authorize_token_url` URL in the browser (or embedded web-view):

    GET /oauth/authorize?oauth_token={req-token}

If the user has used this app before, in conjunction with the current
record-id, the container may silently approve the token. If not, a UI should be
displayed asking the user for permission. If permission is granted, the
container redirects the browser to the URL provided as `oauth_callback` in the
app manifest, adding the verifier:

    {callback-url}?oauth_token={req-token}&oauth_verifier={verifier}


### 4. Getting an Access Token ###

The request token and verifier can now be traded for an access token. This is
achieved by issuing a POST call to the `exchange_token_url`:

    POST /oauth/access_token

Including the complete set of OAuth parameters in the **Authorization** header:

    oauth_consumer_key={consumer-key}
    oauth_nonce={oauth:nonce}
    oauth_signature_method=HMAC-SHA1
    oauth_timestamp={oauth:timestamp}
    oauth_token={req-token}
    oauth_verifier={verifier}
    oauth_version=1.0
    oauth_signature={oauth:signature}

If the call was successful, an HTTP status code `200` is returned and the
access token with secret, the record-id and the user-id can be found in the
body:

    oauth_token={acc-token}&
    oauth_token_secret={acc-secret}&
    record_id={record-id}&
    user_id={user-id}

If the token was not granted, the status code will be `403`.


### 5. Requesting Data ###

All REST calls to the SMART container can now be signed with the access token:

    oauth_consumer_key={consumer-key}
    oauth_nonce={oauth:nonce}
    oauth_signature_method=HMAC-SHA1
    oauth_timestamp={oauth:timestamp}
    oauth_token={acc-token}
    oauth_version=1.0
    oauth_signature={oauth:signature}


As a final note, please use an existing OAuth library for your project instead
of rolling your own!


### Debugging OAuth Problems ###

If you succeed in getting an access token, but the server subsequently rejects
your signed requests, use our debug endpoint to get more information about what
is going wrong with your request.

Send a signed request to:

    http://sandbox-api-v06.smartplatforms.org/oauth/debug


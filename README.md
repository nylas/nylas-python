# Nylas Python SDK 

The Nylas Python SDK provides all of the functionality of the Nylas [REST API](https://docs.nylas.com/reference) in an easy-to-use Python API. With the SDK, you can programmatically access an email account (e.g. Gmail, Yahoo, etc.) and perform functionality such as getting messages and listing message threads.

# Table of Contents

* [Install](#install)
* [Usage](#usage)
* [Quick Start](#quick-start)
* [Open-Source Sync Engine](#open-source-sync-engine)
* [Contributing](#contributing)

# Install

This library is available on [pypi](https://pypi.org/). You can install it by running:

```shell
pip install nylas
```

# Usage

Every resource (i.e. messages, events, contacts, etc.) is accessed via an instance of ```APIClient```. Before making any requests, obtain a reference to ```APIClient``` passing in your APP ID and APP Secret, and then invoke [```authentication_url```](https://docs.nylas.com/reference#oauthauthorize) to redirect the user to an authentication screen.

**Note:** Set the values for ```APP_ID``` and ```APP_SECRET``` to the Client ID and Client Secret that were assigned to your Nylas app in the Nylas dashboard. Although the naming convention differs between the dashboard and API parameters, they both mean the same thing.

```python
from flask import Flask, session, request, redirect, Response
from nylas import APIClient

@app.route('/')
def index():
    redirect_url = "http://0.0.0.0:8888/login_callback"
    client = APIClient(APP_ID, APP_SECRET)
    return redirect(client.authentication_url(redirect_url, scopes='email.read_only,email.send'))
```

Handle the authentication response which provides an access code, and invoke [```token_for_code```](https://docs.nylas.com/reference#oauthtoken) to exchange the code for an access token:

```python
@app.route('/login_callback')
def login_callback():
    if 'error' in request.args:
        return "Login error: {0}".format(request.args['error'])

    # Exchange the authorization code for an access token
    client = APIClient(APP_ID, APP_SECRET)
    code = request.args.get('code')
    session['access_token'] = client.token_for_code(code)
```

You can then use the API to access the account. The following example prints information about the client's email account:

```python
client = APIClient(APP_ID, APP_SECRET, token)

# Print out the email address and provider (Gmail, Exchange)
print(client.account.email_address)
print(client.account.provider)
```

# Quick Start

A quick start tutorial on how to get up and running with the SDK is available [here](https://docs.nylas.com/docs/python-quick-start).

# Open-Source Sync Engine

The [Nylas Sync Engine](http://github.com/nylas/sync-engine) is open source, and you can also use the Python library with the open source API. Since the open source API provides no authentication or security, connecting to it is simple. When you instantiate the Nylas object, set the App ID, App Secret, and API Token to `null`, and pass the fully-qualified address of your copy of the sync engine:

```python
from nylas import APIClient
client = APIClient(None, None, None, 'http://localhost:5555/')

# Get the id of the first account -- this is the access token we're
# going to use.
account_id = client.accounts.first().id

# Display the contents of the first message for the first account
client = APIClient(None, None, account_id, 'http://localhost:5555/')
print(client.messages.first().body)
```

# Contributing

We'd love your help making Nylas better. You can email us at [support@nylas.com](mailto:support@nylas.com).

Please sign the [Contributor License Agreement](https://goo.gl/forms/lKbET6S6iWsGoBbz2) before submitting pull requests. (It's similar to other projects, like NodeJS or Meteor.)

## Releasing a New Version

We have a two-step process for releasing a new version of the Python SDK. Remember that people depend on this library not breaking, so don't cut corners.

1. Run the unit tests:

```shell
python setup.py test`
```

2. Create a new release:

```shell
python setup.py release <major/minor/patch>
git log # to verify
twine upload --repository-url https://test.pypi.org/legacy/ dist/* # push to TestPypi
twine upload dist/* # push to Pypi
git push --tags # update the release tags on GitHub.
```

## Looking for inbox.py?

If you're looking for Kenneth Reitz's SMTP project, please update your `requirements.txt` file to use `inbox.py` or see the [Inbox.py repo on GitHub](https://github.com/kennethreitz/inbox.py).

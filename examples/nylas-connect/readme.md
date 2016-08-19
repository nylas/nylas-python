# Nylas Connect

This tiny flask app is a simple example of how to use Nylas' [Native
authentication APIs](https://www.nylas.com/docs/platform#native_authentication).
It shows how to receive a `refresh_token` from Google before authenticating with
Nylas.

While this steps through the Google OAuth flow manually, you can alternatively
use Google API SDKs for Python and many other languages. Learn more about that
[here](https://developers.google.com/api-client-library/python/). You can also
learn more about Google OAuth
[here](https://developers.google.com/identity/protocols/OAuth2WebServer).

# Getting Started

## Dependencies

### ngrok

[ngrok](https://ngrok.com/) makes it really easy to test callback urls that are
running locally on your computer. 

Start ngrok with the same port that the local flask application is running.

### virtualenv 

Make sure `virtualenv` is installed. To install it type the following:

```bash
pip install virtualenv
```

## Initial Setup

Add your google and nylas client id's and secrets to a new file credentials.py.
See `credentials.py.template` for an example


Create a virtual env, activate it, and then instal python dependencies

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

# Running the app

First, make sure ngrok is running 

```bash
ngrok http 1234
```

Next, run the flask app.
```bash
./app.py
```

Visit http://localhost:1234 in your browser.

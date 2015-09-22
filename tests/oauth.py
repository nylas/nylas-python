#!/usr/bin/env python

import time
from flask import Flask, url_for, session, request, redirect, Response

from nylas import APIClient

try:
    from credentials import APP_ID, APP_SECRET
except ImportError:
    print "Couldn't import credentials.py --- you'll need to create it."
    print "See credentials.py.template for more details."
    sys.exit(-1)

app = Flask(__name__)
app.debug = True
app.secret_key = 'secret'

assert APP_ID != 'YOUR_APP_ID' or APP_SECRET != 'YOUR_APP_SECRET',\
    "You should change the value of APP_ID and APP_SECRET"


@app.route('/')
def index():
    # We don't have an access token, so we're going to use OAuth to
    # authenticate the user

    # Ask flask to generate the url corresponding to the login_callback
    # route. This is similar to using reverse() in django.
    redirect_uri = url_for('.login_callback', _external=True)

    client = APIClient(APP_ID, APP_SECRET)
    return redirect(client.authentication_url(redirect_uri))


@app.route('/login_callback')
def login_callback():
    if 'error' in request.args:
        return "Login error: {0}".format(request.args['error'])

    # Exchange the authorization code for an access token
    client = APIClient(APP_ID, APP_SECRET)
    code = request.args.get('code')
    token = client.token_for_code(code)
    return token

if __name__ == '__main__':
    print "\033[94mOauth self-test. Please browse to http://localhost:5555 and make\033[0m"
    print "\033[94msure that you're seeing a valid API token.\033[0m"

    app.run(host='0.0.0.0', port=5555)

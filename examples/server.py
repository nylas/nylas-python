#!/usr/bin/env python
from flask import Flask, url_for, session, request, redirect

from inbox.client import APIClient

APP_ID = 'a1xtxfwqk6feg9gcr2ixevvku'
APP_SECRET = 'bd1pzi5pvkkb7xrk8n2870txr'

app = Flask(__name__)
app.debug = True
app.secret_key = 'secret'


@app.route('/')
def index():
    if 'access_token' in session:
        return "authorized ok. access_token: " + session['access_token']

    # If no access token, redirect through inbox to get one
    client = APIClient(APP_ID, APP_SECRET)
    redirect_uri = url_for('.login_callback', _external=True)
    return redirect(client.authentication_url(redirect_uri))


@app.route('/login_callback')
def login_callback():
    if 'error' in request.args:
        return "Login error: {0}".format(request.args['error'])

    # Exchange the authorization code for an access token
    client = APIClient(APP_ID, APP_SECRET)
    code = request.args.get('code')
    session['access_token'] = client.auth_code_for_token(code)
    return index()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)

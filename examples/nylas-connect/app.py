#!/usr/bin/env python
import json
import sys
import os
import flask
import requests
import urllib
import logging
import subprocess

from nylas import APIClient

# Sets the logging format
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

try:
    from credentials import *
except ImportError:
    log.error("Couldn't import credentials.py --- you'll need to create it.")
    log.error("See credentials.py.template for more details.")
    sys.exit(-1)

app = flask.Flask(__name__)

# These are the permissions your app will ask the user to approve for access
# https://developers.google.com/identity/protocols/OAuth2WebServer#scope
GOOGLE_SCOPES = ' '.join(['https://mail.google.com/',
                  'https://www.googleapis.com/auth/calendar',
                  'https://www.googleapis.com/auth/userinfo.email',
                  'https://www.googleapis.com/auth/userinfo.profile',
                  'https://www.googleapis.com/auth/calendar',
                  'https://www.google.com/m8/feeds/'])

# This is the path in your Google application that users are redirected to after they
# have authenticated with Google, and it must be authorized through Google's
# developer console
REDIRECT_URI = '' # Note: Use your ngrok url here if testing locally
NYLAS_API = 'https://api.nylas.com'
OAUTH_TOKEN_VALIDATION_URL = 'https://www.googleapis.com/oauth2/v2/tokeninfo'


@app.route('/')
def index():
    if 'google_credentials' not in flask.session:
        return flask.render_template('index.html')

    # The user has authorized with google at this point but we will need to
    # connect the account to Nylas
    if 'nylas_access_token' not in flask.session:
        google_credentials = flask.session['google_credentials']
        google_access_token = google_credentials['access_token']
        email_address = get_email(google_access_token)
        google_refresh_token = google_credentials['refresh_token']
        connect_to_nylas(google_refresh_token, email_address)
        return flask.redirect(flask.url_for('index'))

    # Google account has been setup, let's use Nylas' python SDK to retrieve an
    # email
    client = APIClient(NYLAS_CLIENT_ID, NYLAS_CLIENT_SECRET,
                       flask.session['nylas_access_token'])

    # Display the latest email message!
    return client.threads.first().messages.first().body


# This is the url Google will call once a user has approved access to their
# account
@app.route('/oauth2callback')
def oauth2callback():
  if 'code' not in flask.request.args:
    params = {'response_type': 'code',
                  'access_type':   'offline',
                  'client_id': GOOGLE_CLIENT_ID,
                  'redirect_uri':  REDIRECT_URI,
                  'scope':         GOOGLE_SCOPES,
                  # Note: this is only for testing to ensure a refresh token is
                  # passed everytime, but requires the user to approve offline
                  # access every time. You should remove this if you don't want
                  # your user to have to approve access each time they connect
                  'prompt': 'consent',
                  }
    url_params = urllib.urlencode(params)
    auth_uri = 'https://accounts.google.com/o/oauth2/v2/auth?{}'.format(url_params)
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    data = {'code': auth_code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'}
    r = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data)
    # This refresh token will only be returned once unless you prompt the user
    # for consent every time, so be sure to remember it!
    flask.session['google_credentials'] = r.json()
    return flask.redirect(flask.url_for('index'))


# Connecting an account is a two step process once you have a refresh token from
# Google.
# First POST to /connect/authorize to get an authorization code from Nylas
# Then post to /connect/token to get an access_token that can be used to access
# account data
def connect_to_nylas(google_refresh_token, email_address):
    google_settings = {'google_client_id':     GOOGLE_CLIENT_ID,
                       'google_client_secret': GOOGLE_CLIENT_SECRET,
                       'google_refresh_token': google_refresh_token
                       }

    data = {'client_id':     NYLAS_CLIENT_ID,
            'name':          'Your Name',
            'email_address': email_address,
            'provider':      'gmail',
            'settings':      google_settings
            }
    code = nylas_code(data)

    data = {'client_id':     NYLAS_CLIENT_ID,
            'client_secret': NYLAS_CLIENT_SECRET,
            'code':          code
            }
    nylas_access_token = nylas_token(data)

    flask.session['nylas_access_token'] = nylas_access_token


# Uses googles tokeninfo endpoint to get an email address from the google
# access_token
def get_email(google_access_token):
    r = requests.get(OAUTH_TOKEN_VALIDATION_URL,
        params={'access_token': google_access_token,
                'fields': 'email'}) # specify we only want the email
    resp = r.json()
    log.info(resp)
    return resp['email']


def nylas_code(data):
    connect_uri = '{}/connect/authorize'.format(NYLAS_API)
    resp = requests.post(connect_uri, json=data).json()
    log.info(resp)
    if 'code' in resp:
        return resp['code']

    raise Exception("Error getting auth code from Nylas", err=resp)


def nylas_token(data):
    token_uri = '{}/connect/token'.format(NYLAS_API)
    resp = requests.post(token_uri, json=data).json()
    log.info(resp)
    if 'access_token' in resp:
        return resp['access_token']

    raise Exception("Error getting access token from Nylas", err=resp)


# Setup ngrok and google developer settings to ensure everything works locally 
def initialize():
    # Make sure ngrok is running
    try:
        resp = requests.get('http://localhost:4040/api/tunnels').json()
    except requests.exceptions.ConnectionError:
        print "It looks like ngrok isn't running! Make sure you've started that first with 'ngrok http 1234'"
        sys.exit(-1)

    global REDIRECT_URI
    REDIRECT_URI = "{}/oauth2callback".format(resp['tunnels'][0]['public_url'])
    print REDIRECT_URI
    s = raw_input("Have you added the url above as an authorized callback "
                  "in Google's Developer console? y/n ")
    if s != "y":
        print "You need to set that up first!"
        print "See https://support.nylas.com/hc/en-us/articles/222176307-Google-OAuth-Setup-Guide for more information"
        sys.exit(-1)


if __name__ == '__main__':
  logging.info("Initializing Application")
  import uuid
  initialize()
  app.secret_key = str(uuid.uuid4())
  app.debug = False
  print "Visit http://localhost:1234 in your browser"
  app.run(port=1234)

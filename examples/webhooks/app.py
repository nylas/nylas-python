#!/usr/bin/env python
import sys
import json
import flask
import requests
import hmac
import hashlib

try:
    from credentials import *
except ImportError:
    log.error("Couldn't import credentials.py --- you'll need to create it.")
    log.error("See credentials.py.template for more details.")
    sys.exit(-1)

app = flask.Flask(__name__)


@app.route('/webhook', methods=['GET', 'POST'])
def index():
    # Nylas will check to make sure your webhook is valid by making a GET
    # request to your endpoint with a challenge parameter when you add the
    # endpoint to the developer dashboard.  All you have to do is return the
    # value of the challenge parameter in the body of the response.
    if flask.request.method == 'GET' and 'challenge' in flask.request.args:
        return flask.request.args['challenge']
    # Nylas sent us a webhook notification for some kind of event, so we should
    # process it!
    elif flask.request.method == 'POST':
        # Verify the request to make sure it's actually from Nylas.
        if not verify_request(flask.request):
            return "X-Nylas-Signature failed verification", 401
        # Nylas will send us a json object of the deltas.
        data = json.loads(flask.request.data)
        for delta in data['deltas']:
            # Print some of the information Nylas sent us. This is where you
            # would normally process the webhook notification and do things like
            # fetch relevant message ids, update your database, etc.
            print "{} at {} with id {}".format(delta['type'], delta['date'],
                    delta['object_data']['id'])
        # Don't forget to let Nylas know that everything was pretty ok.
        return "Success", 200

    else:
        # We only allow GET and POST requests to this endpoint.
        return "Method not allowed", 405


# Each request made by Nylas includes an X-Nylas-Signature header. The header
# contains the HMAC-SHA256 signature of the request body, using your client
# secret as the signing key. This allows your app to verify that the
# notification really came from Nylas.
def verify_request(request):
    digest = hmac.new(NYLAS_CLIENT_SECRET, msg=request.data, digestmod=hashlib.sha256).hexdigest()
    return digest == request.headers.get('X-Nylas-Signature')


# Setup ngrok settings to ensure everything works locally 
def initialize():
    # Make sure ngrok is running
    try:
        resp = requests.get('http://localhost:4040/api/tunnels').json()
    except requests.exceptions.ConnectionError:
        print "It looks like ngrok isn't running! Make sure you've started that first with 'ngrok http 1234'"
        sys.exit(-1)

    global WEBHOOK_URI
    WEBHOOK_URI = "{}/webhook".format(resp['tunnels'][1]['public_url'])


if __name__ == '__main__':
    import uuid
    initialize()
    app.secret_key = str(uuid.uuid4())
    app.debug = False
    print "{}\nAdd the above url to the webhooks page at https://developer.nylas.com".format(WEBHOOK_URI)
    app.run(port=1234)

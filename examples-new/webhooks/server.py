# Imports from the Python standard library
from __future__ import print_function
import os
import sys
import datetime
import textwrap
import hmac
import hashlib

# Imports from third-party modules that this project depends on
try:
    import requests
    from flask import Flask, request, render_template
    from werkzeug.contrib.fixers import ProxyFix
except ImportError:
    message = textwrap.dedent("""
        You need to install the dependencies for this project.
        To do so, run this command:

            pip install -r requirements.txt
    """)
    print(message, file=sys.stderr)
    sys.exit(1)

# This example uses Flask, a micro web framework written in Python.
# For more information, check out the documentation: http://flask.pocoo.org
# Create a Flask app, and load the configuration file.
app = Flask(__name__)
app.config.from_json('config.json')

# Check for dummy configuration values.
# If you are building your own application based on this example,
# you can remove this check from your code.
cfg_needs_replacing = [
    key for key, value in app.config.items()
    if isinstance(value, str) and value.startswith("replace me")
]
if cfg_needs_replacing:
    message = textwrap.dedent("""
        This example will only work if you replace the fake configuration
        values in `config.json` with real configuration values.
        The following config values need to be replaced:
        {keys}
        Consult the README.md file in this directory for more information.
    """).format(keys=", ".join(cfg_needs_replacing))
    print(message, file=sys.stderr)
    sys.exit(1)

# Teach Flask how to find out that it's behind an ngrok proxy
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """
    When the Flask server gets a request at the `/webhook` URL, it will run
    this function. Most of the time, that request will be a genuine webhook
    notification from Nylas. However, it's possible that the request could
    be a fake notification from someone else, trying to fool our app. This
    function needs to verify that the webhook is genuine!
    """
    # When you first tell Nylas about your webhook, it will test that webhook
    # URL with a GET request to make sure that it responds correctly.
    # We just need to return the `challenge` parameter to indicate that this
    # is a valid webhook URL.
    if request.method == "GET" and "challenge" in request.args:
        print(" * Nylas connected to the webhook!")
        return request.args["challenge"]

    # Alright, this is a POST request, which means it's a webhook notification.
    # The question is, is it genuine or fake? Check the signature to find out.
    is_genuine = verify_signature(
        message=request.data,
        key=app.config["NYLAS_OAUTH_CLIENT_SECRET"].encode('utf8'),
        signature=request.headers.get('X-Nylas-Signature'),
    )
    if not is_genuine:
        return "Signature verification failed!", 401

    # Alright, we have a genuine webhook notification from Nylas!
    # Let's find out what it says...
    data = request.get_json()
    for delta in data["deltas"]:
        # This is the part of the code where you would process the information
        # from the webhook notification. Each delta is one change that happened,
        # and might require fetching message IDs, updating your database,
        # and so on.
        #
        # However, because this is just an example project, we'll just print
        # out information about the notification, so you can see what
        # information is being sent.
        kwargs = {
            "type": delta["type"],
            "date": datetime.datetime.fromtimestamp(delta["date"]),
            "object_id": delta["object_data"]["id"],
        }
        print(" * {type} at {date} with ID {object_id}".format(**kwargs))

    # Finally, we have to return a 200 Success response to Nylas, to let them
    # know that we processed the webhook successfully.
    return "Success", 200


def verify_signature(message, key, signature):
    """
    This function will verify the authenticity of a digital signature.
    For security purposes, Nylas includes a digital signature in the headers
    of every webhook notification, so that clients can verify that the
    webhook request came from Nylas and no one else. The signing key
    is your OAuth client secret, which only you and Nylas know.
    """
    digest = hmac.new(key, msg=message, digestmod=hashlib.sha256).hexdigest()
    return digest == signature


@app.route("/")
def index():
    """
    This makes sure that when you visit the root of the website,
    you get a webpage rather than a 404 error.
    """
    return render_template("index.html", ngrok_url=ngrok_url())


def ngrok_url():
    """
    If ngrok is running, it exposes an API on port 4040. We can use that
    to figure out what URL it has assigned, and suggest that to the user.
    https://ngrok.com/docs#list-tunnels
    """
    try:
        ngrok_resp = requests.get("http://localhost:4040/api/tunnels")
    except requests.ConnectionError:
        # I guess ngrok isn't running.
        return None
    ngrok_data = ngrok_resp.json()
    secure_urls = [
        tunnel['public_url'] for tunnel in ngrok_data['tunnels']
        if tunnel['proto'] == 'https'
    ]
    return secure_urls[0]


# When this file is executed, run the Flask web server.
if __name__ == "__main__":
    url = ngrok_url()
    if not url:
        print(
            "Looks like ngrok isn't running! Start it by running "
            "`ngrok http 5000` in a different terminal window, "
            "and then try running this example again.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(" * Webhook URL: {url}/webhook".format(url=url))
    app.run()

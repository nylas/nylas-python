# Imports from the Python standard library
from __future__ import print_function
import os
import sys
import textwrap

# Imports from third-party modules that this project depends on
try:
    import requests
    from flask import Flask, render_template
    from werkzeug.contrib.fixers import ProxyFix
    from flask_dance.contrib.nylas import make_nylas_blueprint, nylas
except ImportError:
    message = textwrap.dedent(
        """
        You need to install the dependencies for this project.
        To do so, run this command:

            pip install -r requirements.txt
    """
    )
    print(message, file=sys.stderr)
    sys.exit(1)

try:
    from nylas import APIClient
except ImportError:
    message = textwrap.dedent(
        """
        You need to install the Nylas SDK for this project.
        To do so, run this command:

            pip install nylas
    """
    )
    print(message, file=sys.stderr)
    sys.exit(1)

# This example uses Flask, a micro web framework written in Python.
# For more information, check out the documentation: http://flask.pocoo.org
# Create a Flask app, and load the configuration file.
app = Flask(__name__)
app.config.from_json("config.json")

# Check for dummy configuration values.
# If you are building your own application based on this example,
# you can remove this check from your code.
cfg_needs_replacing = [
    key
    for key, value in app.config.items()
    if isinstance(value, str) and value.startswith("replace me")
]
if cfg_needs_replacing:
    message = textwrap.dedent(
        """
        This example will only work if you replace the fake configuration
        values in `config.json` with real configuration values.
        The following config values need to be replaced:
        {keys}
        Consult the README.md file in this directory for more information.
    """
    ).format(keys=", ".join(cfg_needs_replacing))
    print(message, file=sys.stderr)
    sys.exit(1)

# Use Flask-Dance to automatically set up the OAuth endpoints for Nylas.
# For more information, check out the documentation: http://flask-dance.rtfd.org
nylas_bp = make_nylas_blueprint()
app.register_blueprint(nylas_bp, url_prefix="/login")

# Teach Flask how to find out that it's behind an ngrok proxy
app.wsgi_app = ProxyFix(app.wsgi_app)

# Define what Flask should do when someone visits the root URL of this website.
@app.route("/")
def index():
    # If the user has already connected to Nylas via OAuth,
    # `nylas.authorized` will be True. Otherwise, it will be False.
    if not nylas.authorized:
        # OAuth requires HTTPS. The template will display a handy warning,
        # unless we've overridden the check.
        return render_template(
            "before_authorized.html",
            insecure_override=os.environ.get("OAUTHLIB_INSECURE_TRANSPORT"),
        )

    # If we've gotten to this point, then the user has already connected
    # to Nylas via OAuth. Let's set up the SDK client with the OAuth token:
    client = APIClient(
        client_id=app.config["NYLAS_OAUTH_CLIENT_ID"],
        client_secret=app.config["NYLAS_OAUTH_CLIENT_SECRET"],
        access_token=nylas.access_token,
    )

    # We'll use the Nylas client to fetch information from Nylas
    # about the current user, and pass that to the template.
    account = client.account
    return render_template("after_authorized.html", account=account)


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
        tunnel["public_url"]
        for tunnel in ngrok_data["tunnels"]
        if tunnel["proto"] == "https"
    ]
    return secure_urls[0]


# When this file is executed, run the Flask web server.
if __name__ == "__main__":
    url = ngrok_url()
    if url:
        print(" * Visit {url} to view this Nylas example".format(url=url))

    app.run()

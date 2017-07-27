# Imports from the Python standard library
from __future__ import print_function
import os
import sys
import textwrap

# Imports from third-party modules that this project depends on
try:
    import requests
    from flask import Flask, render_template, session, redirect, url_for
    from werkzeug.contrib.fixers import ProxyFix
    from flask_dance.contrib.google import make_google_blueprint, google
except ImportError:
    message = textwrap.dedent("""
        You need to install the dependencies for this project.
        To do so, run this command:

            pip install -r requirements.txt
    """)
    print(message, file=sys.stderr)
    sys.exit(1)

try:
    from nylas import APIClient
except ImportError:
    message = textwrap.dedent("""
        You need to install the Nylas SDK for this project.
        To do so, run this command:

            pip install nylas
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

# Use Flask-Dance to automatically set up the OAuth endpoints for Google.
# For more information, check out the documentation: http://flask-dance.rtfd.org
google_bp = make_google_blueprint(
    scope=[
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://mail.google.com/",
        "https://www.google.com/m8/feeds",
        "https://www.googleapis.com/auth/calendar",
    ],
    offline=True,  # this allows you to get a refresh token from Google
    redirect_to="after_google",
    # If you get a "missing Google refresh token" error, uncomment this line:
    # reprompt_consent=True,

    # That `reprompt_consent` argument will force Google to re-ask the user
    # every single time if they want to connect with your application.
    # Google will only send the refresh token if the user has explicitly
    # given consent.
)
app.register_blueprint(google_bp, url_prefix="/login")

# Teach Flask how to find out that it's behind an ngrok proxy
app.wsgi_app = ProxyFix(app.wsgi_app)

# Define what Flask should do when someone visits the root URL of this website.
@app.route("/")
def index():
    # If the user has already connected to Google via OAuth,
    # `google.authorized` will be True. We also need to be sure that
    # we have a refresh token from Google. If we don't have both of those,
    # that indicates that we haven't correctly connected with Google.
    if not (google.authorized and "refresh_token" in google.token):
        # Google requires HTTPS. The template will display a handy warning,
        # unless we've overridden the check.
        return render_template(
            "before_google.html",
            insecure_override=os.environ.get("OAUTHLIB_INSECURE_TRANSPORT"),
        )

    if "nylas_access_token" not in session:
        # The user has already connected to Google via OAuth,
        # but hasn't yet passed those credentials to Nylas.
        # We'll redirect the user to the right place to make that happen.
        return redirect(url_for("after_google"))

    # If we've gotten to this point, then the user has already connected
    # to both Google and Nylas.
    # Let's set up the SDK client with the OAuth token:
    client = APIClient(
        app_id=app.config["NYLAS_OAUTH_API_ID"],
        app_secret=app.config["NYLAS_OAUTH_API_SECRET"],
        access_token=session["nylas_access_token"],
    )

    # We'll use the Nylas client to fetch information from Nylas
    # about the current user, and pass that to the template.
    account = client.account
    return render_template("after_connected.html", account=account)


@app.route("/google/success")
def after_google():
    """
    This just renders a confirmation page, to let the user know that
    they've successfully connected to Google and need to move on to the
    next step: passing those authentication credentials to Nylas.
    """
    return render_template("after_google.html")


@app.route("/nylas/connect")
def pass_creds_to_nylas():
    """
    This view loads the credentials from Google and passes them to Nylas,
    to set up native authentication.
    """
    # If you haven't already connected with Google, this won't work.
    if not google.authorized:
        return "Error: not yet connected with Google!", 400

    if "refresh_token" not in google.token:
        # We're missing the refresh token from Google, and the only way to get
        # a new one is to force reauthentication. That's annoying.
        return (
            "Error: missing Google refresh token. "
            "Uncomment the `reprompt_consent` line in the code to fix this."
        ), 500

    # Look up the user's name and email address from Google.
    google_resp = google.get("/oauth2/v2/userinfo?fields=name,email")
    assert google_resp.ok, "Received failure response from Google userinfo API"
    google_userinfo = google_resp.json()

    # Start the connection process by looking up all the information that
    # Nylas needs in order to connect, and sending it to the authorize API.
    nylas_authorize_data = {
        "client_id": app.config["NYLAS_OAUTH_API_ID"],
        "name": google_userinfo["name"],
        "email_address": google_userinfo["email"],
        "provider": "gmail",
        "settings": {
            "google_client_id": app.config["GOOGLE_OAUTH_CLIENT_ID"],
            "google_client_secret": app.config["GOOGLE_OAUTH_CLIENT_SECRET"],
            "google_refresh_token": google.token["refresh_token"],
        }
    }
    nylas_authorize_resp = requests.post(
        "https://api.nylas.com/connect/authorize",
        json=nylas_authorize_data,
    )
    assert nylas_authorize_resp.ok, "Received failure response from Nylas authorize API"
    nylas_code = nylas_authorize_resp.json()["code"]

    # Now that we've got the `code` from the authorize response,
    # pass it to the token response to complete the connection.
    nylas_token_data = {
        "client_id": app.config["NYLAS_OAUTH_API_ID"],
        "client_secret": app.config["NYLAS_OAUTH_API_SECRET"],
        "code": nylas_code,
    }
    nylas_token_resp = requests.post(
        "https://api.nylas.com/connect/token",
        json=nylas_token_data,
    )
    assert nylas_token_resp.ok, "Received failure response from Nylas token API"
    nylas_access_token = nylas_token_resp.json()["access_token"]

    # Great, we've connected Google to Nylas! In the process, Nylas gave us
    # an OAuth access token, which we'll need in order to make API requests
    # to Nylas in the future. We'll save that access token in the Flask session,
    # so we can pick it up later and use it when we need it.
    session["nylas_access_token"] = nylas_access_token

    # We're all done here. Redirect the user back to the home page,
    # which will pick up the access token we just saved.
    return redirect(url_for("index"))


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
    if url:
        print(" * Visit {url} to view this Nylas example".format(url=url))

    app.run()

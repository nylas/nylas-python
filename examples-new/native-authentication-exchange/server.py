# Imports from the Python standard library
from __future__ import print_function
import os
import sys
import textwrap

# Imports from third-party modules that this project depends on
try:
    import requests
    from flask import Flask, render_template, session, redirect, url_for
    from flask_wtf import FlaskForm
    from wtforms.fields import StringField, PasswordField
    from wtforms.fields.html5 import EmailField
    from wtforms.validators import DataRequired
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


class ExchangeCredentialsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    server_host = StringField('Server Host', validators=[DataRequired()])


class APIError(Exception):
    pass


# Define what Flask should do when someone visits the root URL of this website.
@app.route("/", methods=('GET', 'POST'))
def index():
    form = ExchangeCredentialsForm()
    api_error = None
    if form.validate_on_submit():
        try:
            return pass_creds_to_nylas(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data,
                server_host=form.server_host.data,
            )
        except APIError as err:
            api_error = err.args[0]
    return render_template("index.html", form=form, api_error=api_error)


def pass_creds_to_nylas(name, email, password, server_host):
    """
    Passes Exchange credentials to Nylas, to set up native authentication.
    """
    # Start the connection process by looking up all the information that
    # Nylas needs in order to connect, and sending it to the authorize API.
    nylas_authorize_data = {
        "client_id": app.config["NYLAS_OAUTH_API_ID"],
        "name": name,
        "email_address": email,
        "provider": "exchange",
        "settings": {
            "username": email,
            "password": password,
            "eas_server_host": server_host,
        }
    }
    nylas_authorize_resp = requests.post(
        "https://api.nylas.com/connect/authorize",
        json=nylas_authorize_data,
    )
    if not nylas_authorize_resp.ok:
        message = nylas_authorize_resp.json()["message"]
        raise APIError(message)

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
    if not nylas_token_resp.ok:
        message = nylas_token_resp.json()["message"]
        raise APIError(message)

    nylas_access_token = nylas_token_resp.json()["access_token"]

    # Great, we've connected the Exchange account to Nylas!
    # In the process, Nylas gave us an OAuth access token, which we'll need
    # in order to make API requests to Nylas in the future.
    # We'll save that access token in the Flask session, so we can pick it up
    # later and use it when we need it.
    session["nylas_access_token"] = nylas_access_token

    # We're all done here. Redirect the user back to the success page,
    # which will pick up the access token we just saved.
    return redirect(url_for("success"))


@app.route("/success")
def success():
    if "nylas_account_token" not in session:
        return render_template("missing_token.html")

    client = APIClient(
        app_id=app.config["NYLAS_OAUTH_API_ID"],
        app_secret=app.config["NYLAS_OAUTH_API_SECRET"],
        access_token=session["nylas_access_token"],
    )

    # We'll use the Nylas client to fetch information from Nylas
    # about the current user, and pass that to the template.
    account = client.account
    return render_template("success.html", account=account)


# When this file is executed, run the Flask web server.
if __name__ == "__main__":
    app.run()

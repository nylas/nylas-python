# Example: Native Authentication (Gmail)

This is an example project that demonstrates how to connect to Nylas using the
[Native Authentication](https://docs.nylas.com/reference#native-authentication-1)
flow. Note that different email providers have different native authentication
processes; this example project *only* works with Gmail.

This example uses the [Flask](http://flask.pocoo.org/) web framework to make
a small website, and uses the [Flask-Dance](http://flask-dance.rtfd.org/)
extension to handle the tricky bits of implementing the
[OAuth protocol](https://oauth.net/).
Once the native authentication has been set up, this example website will contact
the Nylas API to learn some basic information about the current user,
such as the user's name and email address. It will display that information
on the page, just to prove that it can fetch it correctly.

In order to successfully run this example, you need to do the following things:

## Get a client ID & client secret from Nylas

To do this, make a [Nylas Developer](https://developer.nylas.com/) account.
You should see your client ID and client secret on the dashboard,
once you've logged in on the
[Nylas Developer](https://developer.nylas.com/) website.

## Get a client ID & client secret from Google

To do this, go to the
[Google Developers Console](https://console.developers.google.com)
and create a project. Then go to the "Library" section and enable the
following APIs: "Gmail API", "Contacts API", "Google Calendar API".
Then go to the "Credentials" section and create a new OAuth client ID.
Select "Web application" for the application type, and click the "Create"
button.

Check out the
[Google OAuth Setup Guide](https://support.nylas.com/hc/en-us/articles/222176307)
on the Nylas support website, for more information.

## Update the `config.json` File

Open the `config.json` file in this directory, and replace the example
values with the real values. You'll need the client ID and client secret
from Nylas, and the client ID and client secret from Google.

You'll also need to replace the example secret key with
any random string of letters and numbers: a keyboard mash will do.

## Set Up HTTPS

The OAuth protocol requires that all communication occur via the secure HTTPS
connections, rather than insecure HTTP connections. There are several ways
to set up HTTPS on your computer, but perhaps the simplest is to use
[ngrok](https://ngrok.com), a tool that lets you create a secure tunnel
from the ngrok website to your computer. Install it from the website, and
then run the following command:

```
ngrok http 5000
```

Notice that ngrok will show you two "forwarding" URLs, which may look something
like `http://ed90abe7.ngrok.io` and `https://ed90abe7.ngrok.io`. (The hash
subdomain will be different for you.) You'll be using the second URL, which
starts with `https`.

Alternatively, you can set the `OAUTHLIB_INSECURE_TRANSPORT` environment
variable in your shell, to disable the HTTPS check. That way, you'll be
able to use `localhost` to refer to your app, instead of an ngrok URL.
However, be aware that you won't be able to do this when you deploy
your app to production, so it's usually a better idea to set up HTTPS properly.

## Set the Authorized Redirect URI for Google

Once you have a HTTPS URL that points to your computer, you'll need to tell
Google about it. On the
[Google Developer Console](https://console.developers.google.com),
click on the "Credentials" section, find the OAuth client that you
already created, and click on the "edit" button on the right side.
There is a section called "Authorized redirect URIs"; this is where
you need to tell Google about your HTTPS URL.
Paste your HTTPS URL into text field, and add `/login/google/authorized`
after it. For example, if your HTTPS URL is `https://ad172180.ngrok.io`, then
you would put `https://ad172180.ngrok.io/login/google/authorized` into
the "Authorized redirect URIs" text field.

Then click the "Done" button to save. Even after you save, it usually takes
Google about 5 minutes to update everything behind the scenes.

## Install the Dependencies

This project depends on a few third-party Python modules, like Flask.
These dependencies are listed in the `requirements.txt` file in this directory.
To install them, use the `pip` tool, like this:

```
pip install -r requirements.txt
```

## Run the Example

Finally, run the example project like this:

```
python server.py
```

Once the server is running, visit the ngrok URL in your browser to test it out!

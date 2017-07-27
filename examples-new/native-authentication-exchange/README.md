# Example: Native Authentication (Exchange)

This is an example project that demonstrates how to connect to Nylas using the
[Native Authentication](https://docs.nylas.com/reference#native-authentication-1)
flow. Note that different email providers have different native authentication
processes; this example project *only* works with Microsoft Exchange.

This example uses the [Flask](http://flask.pocoo.org/) web framework to make
a small website, and uses the [Flask-WTF](https://flask-wtf.readthedocs.io/)
extension to implement an HTML form so the user can type in their
Exchange account information.
Once the native authentication has been set up, this example website will contact
the Nylas API to learn some basic information about the current user,
such as the user's name and email address. It will display that information
on the page, just to prove that it can fetch it correctly.

In order to successfully run this example, you need to do the following things:

## Get an API ID & API Secret from Nylas

To do this, make a [Nylas Developer](https://developer.nylas.com/) account.
You should see your API ID and API Secret on the dashboard, once you've logged
in on the [Nylas Developer](https://developer.nylas.com/) website.

## Update the `config.json` File

Open the `config.json` file in this directory, and replace the example
values with the real values. This is where you'll need the API ID and
API Secret fron Nylas. You'll also need to replace the example secret key with
any random string of letters and numbers: a keyboard mash will do.

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

Once the server is running, visit `http://127.0.0.1:5000/` in your browser
to test it out!

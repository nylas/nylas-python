# Nylas Webhooks

This tiny flask app is a simple example of how to use Nylas' webhooks feature.
This app correctly responds to Nylas' challenge request when you add a webhook
url to the [developer dashboard](https://developer.nylas.com). It also verifies
any webhook notification POST requests by Nylas and prints out some information
about the notification.
 
# Dependencies

## ngrok

[ngrok](https://ngrok.com/) makes it really easy to test callback urls that are
running locally on your computer. 

## virtualenv 

Make sure `virtualenv` is installed. To install it type the following:

```bash
pip install virtualenv
```

# Initial Setup

Create a virtual env, activate it, and then install python dependencies

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

# Running the app

First, make sure ngrok is running with the same port that the local flask app is
running.

```bash
ngrok http 1234
```

Next, run the flask app.

```bash
./app.py
```

Follow the instructions that are printed to the console.

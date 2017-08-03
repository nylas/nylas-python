# Example: Webhooks

This is an example project that demonstrates how to use
[the webhooks feature on Nylas](https://docs.nylas.com/reference#webhooks).
When you run the app and set up a webhook with Nylas, it will print out
some information every time you receive a webhook notification from Nylas.

In order to successfully run this example, you need to do the following things:

## Get a client ID & client secret from Nylas

To do this, make a [Nylas Developer](https://developer.nylas.com/) account.
You should see your client ID and client secret on the dashboard,
once you've logged in on the
[Nylas Developer](https://developer.nylas.com/) website.

## Update the `config.json` File

Open the `config.json` file in this directory, and replace the example
client ID and client secret with the real values that you got from the Nylas
Developer dashboard. You'll also need to replace the example secret key with
any random string of letters and numbers: a keyboard mash will do.

## Set Up HTTPS

Nylas requires that all webhooks be delivered to the secure HTTPS endpoints,
rather than insecure HTTP endpoints. There are several ways
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

## Install the Dependencies

This project depends on a few third-party Python modules.
These dependencies are listed in the `requirements.txt` file in this directory.
To install them, use the `pip` tool, like this:

```
pip install -r requirements.txt
```

## Run the Example

Run the example project like this:

```
python server.py
```

You should see the ngrok URL in the console, and the web server will start
on port 5000.

## Set the Nylas Callback URL

Now that your webhook is all set up and running, you need to tell
Nylas about it. On the [Nylas Developer](https://developer.nylas.com) console,
click on the "Webhooks" tab on the left side, then click the "Add Webhook"
button.
Paste your HTTPS URL into text field, and add `/webhook`
after it. For example, if your HTTPS URL is `https://ad172180.ngrok.io`, then
you would put `https://ad172180.ngrok.io/webhook` into the text field.

Then click the "Create Webhook" button to save.

## Trigger events and see webhook notifications!

Send an email on an account that's connected to Nylas. In a minute or two,
you'll get a webhook notification with information about the event that just
happened!

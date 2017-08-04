# Example: Webhooks

This is an example project that demonstrates how to use
[the webhooks feature on Nylas](https://docs.nylas.com/reference#webhooks).
When you run the app and set up a webhook with Nylas, it will print out
some information every time you receive a webhook notification from Nylas.

In order to successfully run this example, you need to do the following things:

## Install and run redis

[Redis](https://redis.io/) is an in-memory data store. This example uses it
as a message broker for the Celery task queue. You'll need to have it running
on your local computer in order to use the task queue.

If you're using macOS, you can install redis from [Homebrew](https://brew.sh/),
like this:

```
brew install redis
brew services start redis
```

If you're unable to install and run redis, you can still run this example
without the task queue -- keep reading.

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

The config file also has two options related to Celery, which you probably
don't need to modify. `CELERY_BROKER_URL` should point to your running redis
server: if you've got it running on your local computer, you're all set.
However, if you haven't managed to get redis running on your computer, you
can change `CELERY_TASK_ALWAYS_EAGER` to `true`. This will disable the task
queue, and cause all Celery tasks to be run immediately rather than queuing
them for later.

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

## Run the Celery worker (if you're using redis)

The Celery worker will continuously check the task queue to see if there are
any new tasks to be run, and it will run any tasks that it finds. Without at
least one worker running, tasks on the task queue will sit there unfinished
forever. To run a celery worker, pass the `--worker` argument to the `server.py`
script, like this:

```
python server.py --worker
```

Note that if you're not using redis, you don't need to run a Celery worker,
because the tasks will be run immediately rather than put on the task queue.

## Run the Example

While the Celery worker is running, open a new terminal window and run the
Flask web server, like this:

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

If you're using redis, you should see the information about the event in the
terminal window where your Celery worker is running. If you're not using
redis, you should see the information about the event in the terminal window
where your Flask web server is running.

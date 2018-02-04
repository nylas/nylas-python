# Nylas REST API Python bindings [![Build Status](https://travis-ci.org/nylas/nylas-python.svg?branch=master)](https://travis-ci.org/nylas/nylas-python) [![Code Coverage](https://codecov.io/gh/nylas/nylas-python/branch/master/graph/badge.svg)](https://codecov.io/gh/nylas/nylas-python)


Python bindings for the Nylas REST API. https://www.nylas.com/docs

## Installation

This library is available on pypi. You can install it by running `pip install nylas`.

## Examples

There are several example Flask apps in the `examples` directory. You can run them to see how different authentication flows might be implemented.

## Usage

### App ID and Secret

Before you can interact with the Nylas REST API, you need to create a Nylas developer account at [https://www.nylas.com/](https://www.nylas.com/). After you've created a developer account, you can create a new application to generate an App ID / Secret pair.

Generally, you should store your App ID and Secret into environment variables to avoid adding them to source control. The example projects use configuration
files instead, to make it easier to get started.


### Authentication

The Nylas REST API uses server-side (three-legged) OAuth, and this library provides convenience methods to simplify the OAuth process.
Here's how it works:

1. You redirect the user to our login page, along with your App Id and Secret
2. Your user logs in
3. She is redirected to a callback URL of your own, along with an access code
4. You use this access code to get an authorization token to the API

For more information about authenticating with Nylas, visit the [Developer Documentation](https://www.nylas.com/cloud/docs#authentication).

In practice, the Nylas REST API client simplifies this down to two steps.

**Step 1: Redirect the user to Nylas:**

```python
from flask import Flask, session, request, redirect, Response
from nylas import APIClient

@app.route('/')
def index():
    redirect_url = "http://0.0.0.0:8888/login_callback"
    client = APIClient(APP_ID, APP_SECRET)
    return redirect(client.authentication_url(redirect_url))

```

**Step 2: Handle the Authentication Response:**

```python
@app.route('/login_callback')
def login_callback():
    if 'error' in request.args:
        return "Login error: {0}".format(request.args['error'])

    # Exchange the authorization code for an access token
    client = APIClient(APP_ID, APP_SECRET)
    code = request.args.get('code')
    session['access_token'] = client.token_for_code(code)
```

You can also use an OAuth library to simplify the authentication flow,
such as [Python Social Auth](https://python-social-auth.readthedocs.io)
or [Flask-Dance](https://flask-dance.readthedocs.io). This SDK also includes
[an example project that shows you one way you can
implement OAuth](examples/hosted-oauth).

**Revoke a token**

To revoke an access token and remove it from your APIClient's session you can
use the `revoke_token` method on APIClient

```python
  client.revoke_token()
```


### Connecting to an account

```python
client = APIClient(APP_ID, APP_SECRET, token)

# Print out the email address and provider (Gmail, Exchange)
print(client.account.email_address)
print(client.account.provider)
```


### Fetching Threads

```python
# Fetch the first thread
thread = client.threads.first()

# Fetch a specific thread
thread = client.threads.find('ac123acd123ef123')

# List all threads tagged `inbox`
# (paginating 50 at a time until no more are returned.)
for thread in client.threads.values():
    print(thread.subject)

# List the 5 most recent unread threads
for thread in client.threads.where(unread=True, limit=5):
    print(thread.subject)

# List starred threads
for thread in client.threads.where(starred=True):
    print(thread.subject)

# List all threads with 'ben@nylas.com'
for thread in client.threads.where(any_email='ben@nylas.com').values():
    print(thread.subject)
```

### Searching Messages and Threads

You can perform a full-text search to find Messages and Threads that contain
your search query. The search is proxied to the mail-provider.

```python
# Find all threads with the word "nylas"
threads = client.threads.search("nylas")

# Find all messages with the word "nylas"
messages = client.messages.search("nylas")
```

### Working with Threads and Messages

```python
# List thread participants
for participant in thread.participants:
    print(participant["email"])

# Mark as read
thread.mark_as_read()

# Mark as unread
thread.mark_as_unread()

# Star a thread
thread.star()

# Unstar it
thread.unstar()

# Add a new label to a message or thread (Gmail)
important_id = 'aw6p0mya6v3r96vyj8kooxa5v'
message.add_label(important_id)

# Remove a label from a message or thread (Gmail)
important_id = 'aw6p0mya6v3r96vyj8kooxa5v'
message.remove_label(important_id)

# Batch update labels on a message or thread (Gmail)
label_ids = ['aw6p0mya6v3r96vyj8kooxa5v', '2ywxapx5g8vybui7hgpzbr33d']
message.update_labels(label_ids)

# Move a message or thread to a different folder (Non-Gmail)

trash_id = 'ds36ik7o55gdqlvpbrjbg9ovn'
message.update_folder(trash_id)

# List messages
for message in thread.messages.values():
    print(message.subject)

# Get the raw contents of a message
print(message.raw)
```

To get the [expanded message view](https://www.nylas.com/docs/platform#expanded_message_view) that includes convenient header information, include `view='expanded'` in the where clause
```
message = client.messages.where(in_='inbox', view='expanded').first()
message.headers['Message-Id']
message.headers['References']
message.headers['In-Reply-To']
```

### Working with Folders and Labels

The Folders and Labels API replaces the now deprecated Tags API. For Gmail accounts, this API allows you to apply labels to whole threads or individual messages. For providers other than Gmail, you can move threads and messages between folders -- a message can only belong to one folder.

```python
# List labels
for label in client.labels:
    print(label.id, label.display_name)

# Create a label
label = client.labels.create()
label.display_name = 'My Label'
label.save()

# Create a folder
# Note that folders and labels behave identically, except that a message can have many labels but only belong to a single folder.
folder = client.folders.create()
folder.display_name = 'My Folder'
folder.save()

# Rename a folder (or label)

# Note that you can't rename core folders like INBOX, Trash, etc.
folder = client.folders.first()
folder.display_name = 'A Different Folder'
folder.save()
```

### Working with Files

Files can be uploaded via two interfaces. One is providing data directly, another is by providing a stream (e.g. to an open file).

```python
# List files
for file in client.files:
    print(file.filename)

# Create a new file with the stream interface
f = open('test.py', 'r')
myfile = client.files.create()
myfile.filename = 'test.py'
myfile.stream = f
myfile.save()
f.close()

# Create a new file with the data interface
myfile2 = client.files.create()
myfile2.filename = 'test.txt'
myfile2.data = "Hello World."
myfile2.save()
```

Once the files have been created, they can be added to a draft via the `attach()` function.

### Working with Drafts

Drafts can be created, saved and then sent. The following example will create a draft, attach a file to it and then send it.

```python
# Create the attachment
myfile = client.files.create()
myfile.filename = 'test.txt'
myfile.data = "hello world"

# Create a new draft
draft = client.drafts.create()
draft.to = [{'name': 'My Friend', 'email': 'my.friend@example.com'}]
draft.subject = "Here's an attachment"
draft.body = "Cheers mate!"
draft.attach(myfile)

# Send it
try:
    draft.send()
except nylas.client.errors.ConnectionError as e:
    print("Unable to connect to the SMTP server.")
except nylas.client.errors.MessageRejectedError as e:
    print("Message got rejected by the SMTP server!")
    print(e.message)

    # Sometimes the API gives us the exact error message
    # returned by the server. Display it since it can be
    # helpful to know exactly why our message got rejected:
    print(e.server_error)

# Delete a draft
draft = client.drafts.create()
draft.subject = "Delete me"
draft.save()
draft.body = "I really mean it."
draft.delete()
# or:
# client.drafts.delete(draft.id, {'version': draft.version})
```

### Message Tracking Features

If you have webhooks enabled for your developer application you can now access Nylas' [Message Tracking Features](https://www.nylas.com/docs/platform#enabling_tracking) to see when a recipient opens, replies, or clicks links within a message.

```python
# Send a message with tracking enabled
draft = client.drafts.create()
draft.to = [{'name': 'Python SDK open tracking test', 'email': 'inboxapptest415@gmail.com'}]
draft.subject = "Python SDK open tracking test"
draft.body = "Stay polish, stay hungary"
draft.tracking = { 'links': 'false', 'opens': 'true', 'thread_replies': 'true', 'payload':'python sdk open tracking test' }
draft.send()
```

It’s important to note that you must wrap links in `<a>` tags for them to be
tracked. Most email clients automatically “linkify” things that look like links,
like `10.0.0.1`, `tel:5402502334`, or `apple.com`. For links to be tracked
properly, you must linkify the content before sending the draft.


### Working with Events

The following example shows how to create and update an event.

```python
# Get a calendar that's not read only
calendar = filter(lambda cal: not cal.read_only, client.calendars)[0]
# Create the event
ev = client.events.create()
ev.title = "Party at the Ritz"
ev.when = {"start_time": 1416423667, "end_time": 1416448867} # These numbers are UTC timestamps
ev.location = "The Old Ritz"
ev.participants = [{"name": "My Friend", 'email': 'my.friend@example.com'}]
ev.calendar_id = calendar.id
ev.save(notify_participants='true') # notify_participants is sent as a query parameter in the request

# Update it
ev.location = "The Waldorf-Astoria"
ev.save()
```

The following example shows how to delete an event. We will pass the parameter notify_participants to the DELETE request to send the cancellation to the event invitees. See the [Deleting Events](https://www.nylas.com/docs/platform?node#deleting_events) API documentation for more details.

```
# Delete it
client.events.delete(ev.id, notify_participants='true')
```

### Working with Messages, Contacts, Calendars, etc.

Each of the primary collections (contacts, messages, etc.) behaves the same way as `threads`. For example, finding messages with a filter is similar to finding threads:

```python
messages = client.messages.where(to=ben@nylas.com).all()
```

The `where` method accepts a keyword argument for each of the filters documented in the [Nylas Filters Documentation](https://www.nylas.com/docs/api#filters).

Note: Because `from` is a reserved word in Python, to filter by the 'from' field, there are two options:
```python
messages = client.messages.where(from_='email@example.com')
# or
messages = client.messages.where(**{'from': 'email@example.com'})
```

## Account Management

### Account status

It's possible to query the status of all the user accounts registered to an app by using `.accounts`:

```python
accounts = client.accounts
print([(acc.sync_status, acc.account_id, acc.trial, acc.trial_expires) for acc in accounts.all()])
```

## Open-Source Sync Engine

The [Nylas Sync Engine](http://github.com/nylas/sync-engine) is open-source, and you can also use the Python library with the open-source API. Since the open-source API provides no authentication or security, connecting to it is simple. When you instantiate the Nylas object, provide null for the App ID, App Secret, and API Token, and pass the fully-qualified address of your copy of the sync engine:

```python
from nylas import APIClient
client = APIClient(None, None, None, 'http://localhost:5555/')

# Get the id of the first account -- this is the access token we're
# going to use.
account_id = client.accounts.first().id

# Display the contents of the first message for the first account
client = APIClient(None, None, account_id, 'http://localhost:5555/')
print(client.messages.first().body)
```


## Contributing

We'd love your help making Nylas better. We hang out on Slack. [Join the channel here.](http://slack-invite.nylas.com) You can also email [support@nylas.com](mailto:support@nylas.com).

Please sign the [Contributor License Agreement](https://goo.gl/forms/lKbET6S6iWsGoBbz2) before submitting pull requests. (It's similar to other projects, like NodeJS or Meteor.)

### Releasing a new version

We have a two-step process for releasing a new version of the Python SDK. Remember that people depend on this library not breaking, so don't cut corners.

1. Run the unit tests.
    `python setup.py test`

2. Create a new release by doing:

    ```shell
    python setup.py release <major/minor/patch>
    git log # to verify
    python setup.py publish
    git push --tags # update the release tags on GitHub.
    ```

## Looking for inbox.py?

If you're looking for Kenneth Reitz's SMTP project, please update your `requirements.txt` file to use `inbox.py` or see the [Inbox.py repo on GitHub](https://github.com/kennethreitz/inbox.py).

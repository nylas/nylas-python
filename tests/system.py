import json
import re
import pytest
import responses
from nylas import APIClient
from nylas.client.restful_models import Label, Folder
from nylas.client.errors import *

API_URL = 'http://localhost:5555'

client = APIClient(None, None, "1qqlrm3m82toh86nevz0o1l24", 'http://localhost:5555')

count = 0

print "Displaying 10 thread subjects"
for thread in client.threads.items():
    print thread.subject
    count += 1
    if count == 10:
        break

print "Sending an email"
draft = client.drafts.create()
draft.to = [{'name': 'Python SDK test', 'email': 'karim@nylas.com'}]
draft.subject = "Python SDK test"
draft.body = "Stay polish, stay hungary"
draft.send()

print 'Creating an event'
calendar = filter(lambda cal: not cal.read_only, client.calendars)[0]
ev = client.events.create()
ev.title = "Party at the Ritz"
ev.when = {"start_time": 1416423667, "end_time": 1416448867} # These numbers are UTC timestamps
ev.location = "The Old Ritz"
ev.participants = [{'name': 'My Friend', 'email': 'my.friend@example.com'}]
ev.calendar_id = calendar.id
ev.save()

print 'Listing folders'
for label in client.labels:
    print label.display_name

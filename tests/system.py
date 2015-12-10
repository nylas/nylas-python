# -*- coding: utf-8 -*-
import json
import re
import pytest
import time
import datetime
import sys
from nylas import APIClient
from nylas.client.restful_models import Label, Folder
from nylas.client.errors import *
from credentials import APP_ID, APP_SECRET, AUTH_TOKEN

client = APIClient(APP_ID, APP_SECRET, AUTH_TOKEN)

count = 0

print "Listing accounts"
for account in client.accounts:
    print (account.email_address, account.provider)

print 'Marking the first thread as unread'
th = client.threads.where(in_='Boîte de réception').first()
print th.subject
th.mark_as_unread()

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

d1 = datetime.datetime.now() + datetime.timedelta(days=5,hours=4)
d2 = datetime.datetime.now() + datetime.timedelta(days=5,hours=5)

ev.when = {"start_time": time.mktime(d1.timetuple()), "end_time": time.mktime(d2.timetuple())}
ev.location = "The Old Ritz"
ev.participants = [{'name': 'Karim Hamidou', 'email': 'karim@nylas.com'}]
ev.calendar_id = calendar.id
ev.save(notify_participants='true')

print 'Listing folders'
for label in client.labels:
    print label.display_name

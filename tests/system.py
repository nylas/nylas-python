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

print "Listing accounts for application"
for account in client.accounts:
    print (account.email, account.id, account.billing_state, account.sync_state)

print "Listing authenticated API account"
account = client.account
print (account.email_address, account.provider, account.id)

print 'Marking the first thread as unread'
th = client.threads.where({'in': 'inbox'}).first()
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
draft.to = [{'name': 'Python SDK test', 'email': 'inboxapptest415@gmail.com'}]
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
ev.participants = [{'name': 'Nylas Test', 'email': 'inboxapptest415@gmail.com'}]
ev.calendar_id = calendar.id
ev.save(notify_participants='true')

# Send a message with tracking enabled
print 'Send a message with open tracking enabled'
draft = client.drafts.create()
draft.to = [{'name': 'Python SDK open tracking test', 'email': 'inboxapptest415@gmail.com'}]
draft.subject = "Python SDK open tracking test"
draft.body = "Stay polish, stay hungary"
draft.tracking = { 'links': 'false', 'opens': 'true', 'thread_replies': 'true', 'payload':'python sdk open tracking test' }
draft.send()

print "Get expanded view for message"
m = client.messages.where(in_='inbox', limit=1, view='expanded').first()
print m.headers['Message-Id']

print 'Listing folders'
for label in client.labels:
    print label.display_name

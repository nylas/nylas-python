#!/usr/bin/python

import time
from inbox import APIClient
from inbox.util import generate_id

APP_ID = '[YOUR_APP_ID]'
APP_SECRET = '[YOUR_APP_SECRET]'
ACCESS_TOKEN = '[YOUR_ACCESS_TOKEN]'

inbox = APIClient(None, None, api_server='http://localhost:5555')
ns = inbox.namespaces[0]

subject = generate_id()

f = open('test.py', 'r')
data = f.read()
f.close()

myfile = ns.files.create()
myfile.filename = 'test.py'
myfile.data = data

# Create a new draft
draft = ns.drafts.create()
draft.to = [{'name': 'Charles Gruenwald', 'email': 'inboxtestempty@gmail.com'}]
draft.subject = subject
draft.body = ""
draft.attach(myfile)
draft.send()

x = 0
th = ns.threads.where({'tag': 'sent', 'subject': subject}).first()
while not th:
    time.sleep(0.5)
    x += 1
    th = ns.threads.where({'tag': 'sent', 'subject': subject}).first()

m = th.messages[0]

print m.attachments[0].download()

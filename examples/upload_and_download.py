#!/usr/bin/python
from __future__ import print_function
import time
from nylas import APIClient
from nylas.util import generate_id

APP_ID = '[YOUR_APP_ID]'
APP_SECRET = '[YOUR_APP_SECRET]'
ACCESS_TOKEN = '[YOUR_ACCESS_TOKEN]'
client = APIClient(APP_ID, APP_SECRET, ACCESS_TOKEN)

subject = generate_id()

f = open('test.py', 'r')
data = f.read()
f.close()

myfile = client.files.create()
myfile.filename = 'test.py'
myfile.data = data

# Create a new draft
draft = client.drafts.create()
draft.to = [{'name': 'Charles Gruenwald', 'email': 'nylastestempty@gmail.com'}]
draft.subject = subject
draft.body = ""
draft.attach(myfile)
draft.send()

x = 0
th = client.threads.where({'in': 'Sent', 'subject': subject}).first()
while not th:
    time.sleep(0.5)
    x += 1
    th = client.threads.where({'in': 'Sent', 'subject': subject}).first()

m = th.messages[0]

print(m.attachments[0].download())

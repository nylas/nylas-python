#!/usr/bin/python
from __future__ import print_function
import os
import time
from nylas import APIClient
from nylas.util import generate_id

APP_ID = '[YOUR_APP_ID]'
APP_SECRET = '[YOUR_APP_SECRET]'
ACCESS_TOKEN = '[YOUR_ACCESS_TOKEN]'
client = APIClient(APP_ID, APP_SECRET, ACCESS_TOKEN)

subject = generate_id()
# Create a new draft
draft = client.drafts.create()
draft.to = [{'name': 'Nylas PythonSDK', 'email': 'nylastestempty@gmail.com'}]
draft.subject = subject
draft.body = ""

for filename in filter(lambda x: not os.path.isdir(x), os.listdir(".")):
    f = open(filename, 'r')
    attachment = client.files.create()
    attachment.filename = filename
    attachment.stream = f
    attachment.save()
    draft.attach(attachment)

draft.send()

th = client.threads.where({'in': 'Sent', 'subject': subject}).first()
while not th:
    time.sleep(0.5)
    th = client.threads.where({'in': 'Sent', 'subject': subject}).first()

print(th.messages[0].attachments[0].download())

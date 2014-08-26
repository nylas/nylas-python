#!/usr/bin/python

from operator import itemgetter
from inbox import APIClient

APP_ID = '[YOUR_APP_ID]'
APP_SECRET = '[YOUR_APP_SECRET]'
ACCESS_TOKEN = '[YOUR_ACCESS_TOKEN]'
inbox = APIClient(APP_ID, APP_SECRET, ACCESS_TOKEN)

counts = {}

total = 0
for th in client.namespaces[0].threads.items():
    for m in th.messages.items():
        for p in map(lambda x: x['email'], m['from']):
            if p not in counts:
                counts[p] = 0
            counts[p] += 1

most_chatted = sorted(counts.iteritems(), key=itemgetter(1))
for i in most_chatted:
    print i

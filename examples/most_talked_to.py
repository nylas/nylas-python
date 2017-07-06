#!/usr/bin/python
from __future__ import print_function
from operator import itemgetter
from nylas import APIClient

APP_ID = '[YOUR_APP_ID]'
APP_SECRET = '[YOUR_APP_SECRET]'
ACCESS_TOKEN = '[YOUR_ACCESS_TOKEN]'
client = APIClient(APP_ID, APP_SECRET, ACCESS_TOKEN)

counts = {}

for m in client.messages:
	for p in map(lambda x: x['email'], m['from']):
		if p not in counts:
			counts[p] = 0
		counts[p] += 1

most_chatted = sorted(counts.iteritems(), key=itemgetter(1))
for i in most_chatted:
    print(i)

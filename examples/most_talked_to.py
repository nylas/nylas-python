#!/usr/bin/python

from operator import itemgetter
from inbox import APIClient

APP_ID = 'a1xtxfwqk6feg9gcr2ixevvku'
APP_SECRET = 'bd1pzi5pvkkb7xrk8n2870txr'
ACCESS_TOKEN = 'PjHcduuK03mYGBLwZTADV3IQDFES5f'

ACCESS_TOKEN = 'io4b2p6t3ndozs5b1hyf7TbJopgB7B'
ACCESS_TOKEN = 'I2kR65MmTEnAAiZ30bFqW5rEvK3Ybg'
client = APIClient(APP_ID, APP_SECRET, ACCESS_TOKEN)

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

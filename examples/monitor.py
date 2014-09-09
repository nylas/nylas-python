#!/usr/bin/env python
import sys
import click
import json
from time import time, sleep
from inbox import APIClient
from inbox.client.util import generate_id
import sys

TIMEOUT = 120


class TimeoutError(Exception):
    pass


def self_send(client, email):
    draft = client.drafts.create(to=[{'name': 'Inbox SelfSend',
                                      'email': email}],
                                 subject=generate_id())
    draft.send()

    start = time()
    while time() - start < TIMEOUT:
        th = client.threads.where(tag='sent', subject=draft.subject).first()
        if th:
            return th
        sleep(0.1)
    raise TimeoutError()


def self_receive(client, thread):
    start = time()
    while time() - start < TIMEOUT:
        for th in client.threads.where(subject=thread.subject):
            if 'inbox' in [t['name'] for t in th.tags]:
                return th
        sleep(0.1)
    raise TimeoutError()


def remove(client, thread):
    thread.archive()

    start = time()
    while time() - start < TIMEOUT:
        if not len(client.threads.where(tag='inbox',
                                        subject=thread.subject).all()):
            return
        sleep(0.1)
    raise TimeoutError()


def do_run(email, access_token):
    client = APIClient(access_token=access_token)
    stats = {'email': email}

    start = time()
    client.contacts.where(limit=100).all()
    stats['contacts'] = time() - start

    start = time()
    client.threads.where(limit=100).all()

    stats['threads'] = time() - start

    start = time()
    th = self_send(client, email)
    stats['send'] = time() - start

    start = time()
    th = self_receive(client, th)
    stats['recv'] = time() - start

    start = time()
    remove(client, th)
    stats['trash'] = time() - start
    return stats


@click.command()
@click.option('--email', default=None, help='Email address')
@click.option('--access_token', default=None, help='Access token')
def main(email, access_token):
    stats = do_run(email, access_token)
    print json.dumps(stats)


if __name__ == '__main__':
        main()

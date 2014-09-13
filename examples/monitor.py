#!/usr/bin/env python
import sys
import click
import json
import random
from time import time, sleep
from inbox import APIClient
from inbox.client.util import generate_id
from inbox.client.errors import APIClientError
from lib.random_words import random_words
import sys

TIMEOUT = 900
QUERY_THRESHOLD = 6.0

current_operation = ""


class TimeoutError(Exception):
    pass


def self_send(client, email, random_email):
    draft = client.drafts.create(to=[{'name': 'Inbox SelfSend',
                                      'email': email}],
                                 subject=generate_id())

    if random_email:
        draft.subject = random_words(8, sig=None)
        print "subject: [{}]".format(draft.subject)
        draft.body = random_words(sig=email.split('@')[0])

    draft.send()

    start = time()
    while time() - start < TIMEOUT:
        th = client.threads.where(tag='sent', subject=draft.subject).first()
        if th:
            return th
        sleep(0.1)
    raise TimeoutError(current_operation)


def self_receive(client, thread):
    start = time()
    while time() - start < TIMEOUT:
        for th in client.threads.where(subject=thread.subject):
            if 'inbox' in [t['name'] for t in th.tags]:
                return th
        sleep(0.1)
    raise TimeoutError(current_operation)


def remove(client, thread):
    thread.archive()

    start = time()
    while time() - start < TIMEOUT:
        if not len(client.threads.where(tag='inbox',
                                        subject=thread.subject).all()):
            return
        sleep(0.1)
    raise TimeoutError(current_operation)


def do_run(email, access_token, random_email):
    global current_operation
    client = APIClient(access_token=access_token)
    stats = {'email': email}

    current_operation = 'contacts'
    sys.stdout.flush()
    start = time()
    client.contacts.where(limit=100).all()
    stats[current_operation] = time() - start

    sys.stdout.flush()
    current_operation = 'threads'
    start = time()
    client.threads.where(limit=100).all()
    stats[current_operation] = time() - start
    if stats[current_opartion] > QUERY_THRESHOLD:
        raise TimeoutError(current_operation)

    current_operation = 'send'
    start = time()
    th = self_send(client, email, random_email)
    stats[current_operation] = time() - start

    current_operation = 'recv'
    start = time()
    th = self_receive(client, th)
    stats[current_operation] = time() - start

    current_operation = 'trash'
    start = time()
    remove(client, th)
    stats[current_operation] = time() - start
    return stats


@click.command()
@click.option('--email', default=None, help='Email address')
@click.option('--access_token', default=None, help='Access token')
@click.option('--random_delay', default=False, is_flag=True)
@click.option('--random_email', default=False, is_flag=True)
def main(email, access_token, random_delay, random_email):
    if random_delay:
        sleep(random.uniform(1,60))

    try:
        stats = do_run(email, access_token, random_email)
        print json.dumps(stats)
    except TimeoutError as e:
        print json.dumps({'email': email,
                          'message': "Timed out.",
                          'event': str(e)})
        sys.exit(2)
    except APIClientError as e:
        msg = "Error during: {}".format(current_operation)
        print json.dumps({'email': email,
                          'message': msg,
                          'event': e.as_dict()})
        sys.exit(2)


if __name__ == '__main__':
        main()

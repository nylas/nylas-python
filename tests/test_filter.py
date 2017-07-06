import json
import random
import httpretty
from httpretty import Response


def test_no_filter(api_client, api_url, message_body):
    httpretty.enable()

    message_body_list_50 = [message_body for _ in range(1, 51)]
    message_body_list_22 = [message_body for _ in range(1, 23)]

    # httpretty kind of sucks and strips & parameters from the URL
    values = [
        Response(status=200, body=json.dumps(message_body_list_50)),
        Response(status=200, body=json.dumps(message_body_list_22)),
    ]
    httpretty.register_uri(
        httpretty.GET,
        api_url + '/events',
        responses=values,
    )

    events = api_client.events.all()
    assert len(events) == 72
    assert events[0].id == 'cv4ei7syx10uvsxbs21ccsezf'

    httpretty.disable()


def test_two_filters(api_client, api_url):
    httpretty.enable()

    values2 = [Response(status=200, body='[]')]
    httpretty.register_uri(
        httpretty.GET,
        api_url + '/events?param1=a&param2=b',
        responses=values2,
    )
    events = api_client.events.where(param1='a', param2='b').all()
    assert len(events) == 0  # pylint: disable=len-as-condition
    query = httpretty.last_request().querystring
    assert query['param1'][0] == 'a'
    assert query['param2'][0] == 'b'
    httpretty.disable()

def test_no_offset(api_client, api_url):
    httpretty.enable()

    values = [Response(status=200, body='[]')]
    httpretty.register_uri(
        httpretty.GET,
        api_url + '/events?in=Nylas',
        responses=values,
    )
    list(api_client.events.where({'in': 'Nylas'}).items())
    query = httpretty.last_request().querystring
    assert query['in'][0] == 'Nylas'
    assert query['offset'][0] == '0'
    httpretty.disable()

def test_zero_offset(api_client, api_url):
    httpretty.enable()

    values = [Response(status=200, body='[]')]
    httpretty.register_uri(
        httpretty.GET,
        api_url + '/events?in=Nylas&offset=0',
        responses=values,
    )
    list(api_client.events.where({'in': 'Nylas', 'offset': 0}).items())
    query = httpretty.last_request().querystring
    assert query['in'][0] == 'Nylas'
    assert query['offset'][0] == '0'
    httpretty.disable()

def test_non_zero_offset(api_client, api_url):
    httpretty.enable()

    offset = random.randint(1, 1000)
    values = [Response(status=200, body='[]')]
    httpretty.register_uri(
        httpretty.GET,
        api_url + '/events?in=Nylas&offset=' + str(offset),
        responses=values,
    )
    list(api_client.events.where({'in': 'Nylas', 'offset': offset}).items())
    query = httpretty.last_request().querystring
    assert query['in'][0] == 'Nylas'
    assert query['offset'][0] == str(offset)
    httpretty.disable()

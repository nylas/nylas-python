import json
import pytest
import responses
import httpretty
from httpretty import Response
from conftest import API_URL
from nylas.client.errors import InvalidRequestError


def test_file_upload(api_client):
    httpretty.enable()
    body = [{
        "content_type": "text/plain",
        "filename": "a.txt",
        "id": "3qfe4k3siosfjtjpfdnon8zbn",
        "account_id": "6aakaxzi4j5gn6f7kbb9e0fxs",
        "object": "file",
        "size": 762878
    }]

    values = [Response(status=200, body=json.dumps(body))]
    httpretty.register_uri(httpretty.POST, API_URL + '/files/', responses=values)
    httpretty.register_uri(httpretty.GET, API_URL + '/files/3qfe4k3siosfjtjpfdnon8zbn/download',
                           body='test body')

    myfile2 = api_client.files.create()
    myfile2.filename = 'test.txt'
    myfile2.data = "Hello World."
    myfile2.save()

    assert myfile2.filename == 'a.txt'
    assert myfile2.size == 762878

    data = myfile2.download()
    assert data == 'test body'

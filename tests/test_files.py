import json
import pytest
import responses
import httpretty
from httpretty import Response
from nylas.client.errors import InvalidRequestError, FileUploadError


def test_file_upload(api_client, api_url):
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
    httpretty.register_uri(httpretty.POST, api_url + '/files/', responses=values)
    httpretty.register_uri(httpretty.GET, api_url + '/files/3qfe4k3siosfjtjpfdnon8zbn/download',
                           body='test body')

    myfile = api_client.files.create()
    myfile.filename = 'test.txt'
    myfile.data = "Hello World."
    myfile.save()

    assert myfile.filename == 'a.txt'
    assert myfile.size == 762878

    data = myfile.download().decode()
    assert data == 'test body'


def test_file_upload_errors(api_client):
    myfile = api_client.files.create()
    myfile.filename = 'test.txt'
    myfile.data = "Hello World."

    with pytest.raises(FileUploadError) as exc:
        myfile.download()

    assert exc.value.message == ("Can't download a file that "
                                 "hasn't been uploaded.")

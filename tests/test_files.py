import cgi
from io import BytesIO
import pytest
from nylas.client.errors import FileUploadError


@pytest.mark.usefixtures("mock_files")
def test_file_upload_data(api_client, mocked_responses):
    data = "Hello, World!"

    myfile = api_client.files.create()
    myfile.filename = "hello.txt"
    myfile.data = data

    assert not mocked_responses.calls
    myfile.save()
    assert len(mocked_responses.calls) == 1

    assert myfile.filename == "hello.txt"
    assert myfile.size == 13

    upload_body = mocked_responses.calls[0].request.body
    upload_lines = upload_body.decode("utf8").splitlines()

    content_disposition = upload_lines[1]
    _, params = cgi.parse_header(content_disposition)
    assert params["filename"] == "hello.txt"
    assert "Hello, World!" in upload_lines


@pytest.mark.usefixtures("mock_files")
def test_file_upload_stream(api_client, mocked_responses):
    stream = BytesIO(b"Hello, World!")
    stream.name = "wacky.txt"

    myfile = api_client.files.create()
    myfile.filename = "hello.txt"
    myfile.stream = stream
    assert not mocked_responses.calls
    myfile.save()
    assert len(mocked_responses.calls) == 1

    assert myfile.filename == "hello.txt"
    assert myfile.size == 13

    upload_body = mocked_responses.calls[0].request.body
    upload_lines = upload_body.decode("utf8").splitlines()

    content_disposition = upload_lines[1]
    _, params = cgi.parse_header(content_disposition)
    assert params["filename"] == "hello.txt"
    assert "Hello, World!" in upload_lines


@pytest.mark.usefixtures("mock_files")
def test_file_download(api_client, mocked_responses):
    assert not mocked_responses.calls
    myfile = api_client.files.first()
    assert len(mocked_responses.calls) == 1
    data = myfile.download().decode()
    assert len(mocked_responses.calls) == 2
    assert data == "Hello, World!"


def test_file_invalid_upload(api_client):
    myfile = api_client.files.create()
    with pytest.raises(FileUploadError) as exc:
        myfile.save()

    assert str(exc.value) == (
        "File object not properly formatted, " "must provide either a stream or data."
    )


def test_file_upload_errors(api_client):
    myfile = api_client.files.create()
    myfile.filename = "test.txt"
    myfile.data = "Hello World."

    with pytest.raises(FileUploadError) as exc:
        myfile.download()

    assert str(exc.value) == ("Can't download a file that " "hasn't been uploaded.")

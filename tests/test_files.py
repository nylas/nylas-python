import pytest
from nylas.client.errors import FileUploadError


@pytest.mark.usefixtures("mock_files")
def test_file_upload(api_client):
    myfile = api_client.files.create()
    myfile.filename = 'test.txt'
    myfile.data = "Hello World."
    myfile.save()

    assert myfile.filename == 'a.txt'
    assert myfile.size == 762878

    data = myfile.download().decode()
    assert data == 'test body'


def test_file_invalid_upload(api_client):
    myfile = api_client.files.create()
    with pytest.raises(FileUploadError) as exc:
        myfile.save()

    assert exc.value.message == (
        "File object not properly formatted, "
        "must provide either a stream or data."
    )


def test_file_upload_errors(api_client):
    myfile = api_client.files.create()
    myfile.filename = 'test.txt'
    myfile.data = "Hello World."

    with pytest.raises(FileUploadError) as exc:
        myfile.download()

    assert exc.value.message == ("Can't download a file that "
                                 "hasn't been uploaded.")

import pytest
import responses


@responses.activate
@pytest.mark.usefixtures("mock_threads")
def test_thread_folder(api_client):
    thread = api_client.threads.first()
    assert len(thread.labels) == 0  # pylint: disable=len-as-condition
    assert len(thread.folders) == 1
    assert thread.folders[0].display_name == 'Inbox'
    assert not thread.unread
    assert thread.starred


@responses.activate
@pytest.mark.usefixtures("mock_folder_account", "mock_threads", "mock_thread")
def test_thread_change(api_client):
    thread = api_client.threads.first()

    assert thread.starred
    thread.unstar()
    assert not thread.starred

    thread.update_folder('qwer')
    assert len(thread.folders) == 1
    assert thread.folders[0].id == 'qwer'

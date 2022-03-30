import pytest


@pytest.mark.usefixtures("mock_thread_search_response")
def test_search_threads(api_client):
    threads = api_client.threads.search("Helena")
    assert len(threads) == 1
    assert "Helena" in threads[0].snippet


@pytest.mark.usefixtures("mock_message_search_response")
def test_search_messages(api_client):
    messages = api_client.messages.search("Pinot")
    assert len(messages) == 2
    assert "Pinot" in messages[0].snippet
    assert "Pinot" in messages[1].snippet


@pytest.mark.usefixtures("mock_message_search_response")
def test_search_messages_with_limit_offset(mocked_responses, api_client):
    api_client.messages.search("Pinot", limit=10, offset=0)
    request = mocked_responses.calls[0].request
    assert request.path_url == "/messages/search?q=Pinot&limit=10&offset=0"


@pytest.mark.usefixtures("mock_message_search_response")
def test_search_drafts(api_client):
    with pytest.raises(Exception):
        api_client.drafts.search("Pinot")

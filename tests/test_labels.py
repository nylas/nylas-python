import pytest
from nylas.client.restful_models import Label, Thread, Message


@pytest.mark.usefixtures("mock_labels")
def test_list_labels(api_client):
    labels = api_client.labels
    labels = [l for l in labels]
    assert len(labels) == 5
    assert all(isinstance(x, Label) for x in labels)


@pytest.mark.usefixtures("mock_label")
def test_get_label(api_client):
    label = api_client.labels.get("anuep8pe5ugmxrucchrzba2o8")
    assert label is not None
    assert isinstance(label, Label)
    assert label.display_name == "Important"


@pytest.mark.usefixtures("mock_label", "mock_threads")
def test_label_threads(api_client):
    label = api_client.labels.get("anuep8pe5ugmxrucchrzba2o8")
    assert label.threads
    assert all(isinstance(thread, Thread) for thread in label.threads)


@pytest.mark.usefixtures("mock_label", "mock_messages")
def test_label_messages(api_client):
    label = api_client.labels.get("anuep8pe5ugmxrucchrzba2o8")
    assert label.messages
    assert all(isinstance(message, Message) for message in label.messages)

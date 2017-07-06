import pytest
import responses
from nylas.client.restful_models import Label


@responses.activate
@pytest.mark.usefixtures("mock_labels")
def test_list_labels(api_client):
    labels = api_client.labels
    labels = [l for l in labels]
    assert len(labels) == 5
    assert all(isinstance(x, Label) for x in labels)


@responses.activate
@pytest.mark.usefixtures("mock_label")
def test_get_label(api_client):
    label = api_client.labels.find('anuep8pe5ugmxrucchrzba2o8')
    assert label is not None
    assert isinstance(label, Label)
    assert label.display_name == 'Important'

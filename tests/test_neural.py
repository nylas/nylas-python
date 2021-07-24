import json
from datetime import datetime

import pytest
from nylas.client.restful_models import File

from nylas.client.neural_api_models import (
    NeuralSignatureContact,
    NeuralMessageOptions,
    Categorize,
    NeuralCategorizer,
)


@pytest.mark.usefixtures("mock_sentiment_analysis")
def test_sentiment_analysis_message(mocked_responses, api_client, account_id):
    analysis_response = api_client.neural.sentiment_analysis_message(["message_id"])
    assert len(mocked_responses.calls) == 1
    request = mocked_responses.calls[0].request
    assert json.loads(request.body) == {"message_id": ["message_id"]}
    assert len(analysis_response) == 1
    analysis = analysis_response[0]
    assert analysis.account_id == account_id
    assert analysis.processed_length == 11
    assert analysis.sentiment == "NEUTRAL"
    assert analysis.sentiment_score == 0.30000001192092896
    assert analysis.text == "hello world"


@pytest.mark.usefixtures("mock_sentiment_analysis")
def test_sentiment_analysis_text(mocked_responses, api_client, account_id):
    analysis = api_client.neural.sentiment_analysis_text("hello world")
    assert len(mocked_responses.calls) == 1
    request = mocked_responses.calls[0].request
    assert json.loads(request.body) == {"text": "hello world"}
    assert analysis.account_id == account_id
    assert analysis.processed_length == 11
    assert analysis.sentiment == "NEUTRAL"
    assert analysis.sentiment_score == 0.30000001192092896
    assert analysis.text == "hello world"


@pytest.mark.usefixtures("mock_extract_signature")
def test_extract_signature(mocked_responses, api_client):
    signature_response = api_client.neural.extract_signature(["abc123"])
    assert len(mocked_responses.calls) == 1
    request = mocked_responses.calls[0].request
    assert json.loads(request.body) == {"message_id": ["abc123"]}
    assert len(signature_response) == 1
    signature = signature_response[0]
    assert (
        signature.signature
        == "Nylas Swag\n\nSoftware Engineer\n\n123-456-8901\n\nswag@nylas.com"
    )
    assert signature.model_version == "0.0.1"
    assert isinstance(signature.contacts, NeuralSignatureContact)
    contact = signature.contacts
    assert contact.job_titles == ["Software Engineer"]
    assert contact.links == [
        {
            "description": "string",
            "url": "https://example.com/link.html",
        }
    ]
    assert contact.phone_numbers == ["123-456-8901"]
    assert contact.emails == ["swag@nylas.com"]
    assert contact.names == [
        {
            "first_name": "Nylas",
            "last_name": "Swag",
        }
    ]


@pytest.mark.usefixtures("mock_extract_signature")
def test_extract_signature_options(mocked_responses, api_client):
    options = NeuralMessageOptions(False, False, False, False, False)
    api_client.neural.extract_signature(["abc123"], False, options)
    request = mocked_responses.calls[0].request
    assert json.loads(request.body) == {
        "message_id": ["abc123"],
        "parse_contacts": False,
        "ignore_links": False,
        "ignore_images": False,
        "ignore_tables": False,
        "remove_conclusion_phrases": False,
        "images_as_markdowns": False,
    }


@pytest.mark.usefixtures("mock_extract_signature")
def test_signature_convert_contact(mocked_responses, api_client):
    signature = api_client.neural.extract_signature(["abc123"])
    contact = signature[0].contacts.to_contact_object()
    assert contact.given_name == "Nylas"
    assert contact.surname == "Swag"
    assert contact.job_title == "Software Engineer"
    assert len(contact.emails) == 1
    assert contact.emails["personal"] == ["swag@nylas.com"]
    assert len(contact.phone_numbers) == 1
    assert contact.phone_numbers["mobile"] == ["123-456-8901"]
    assert len(contact.web_pages) == 1
    assert contact.web_pages["string"] == ["https://example.com/link.html"]


@pytest.mark.usefixtures("mock_categorize")
def test_categorize(mocked_responses, api_client):
    response = api_client.neural.categorize(["abc123"])
    assert len(mocked_responses.calls) == 1
    request = mocked_responses.calls[0].request
    assert json.loads(request.body) == {"message_id": ["abc123"]}
    assert len(response) == 1
    assert isinstance(response[0].categorizer, Categorize)
    categorize = response[0].categorizer
    assert categorize.category == "feed"
    assert categorize.model_version == "6194f733"
    assert categorize.subcategories == ["ooo"]
    assert categorize.categorized_at == datetime.utcfromtimestamp(1627076720)


@pytest.mark.usefixtures("mock_categorize")
def test_recategorize(mocked_responses, api_client):
    categorize = api_client.neural.categorize("abc123")
    recategorize = categorize[0].recategorize("conversation")
    assert len(mocked_responses.calls) == 3
    request = mocked_responses.calls[1].request
    assert json.loads(request.body) == {
        "message_id": "abc123",
        "category": "conversation",
    }
    assert isinstance(recategorize, NeuralCategorizer)


@pytest.mark.usefixtures("mock_ocr_request")
def test_ocr_request(mocked_responses, api_client):
    ocr = api_client.neural.ocr_request("abc123", [2, 3])
    assert len(mocked_responses.calls) == 1
    request = mocked_responses.calls[0].request
    assert json.loads(request.body) == {"file_id": "abc123", "pages": [2, 3]}
    assert len(ocr.ocr) == 2
    assert ocr.ocr[0] == "This is page 1"
    assert ocr.ocr[1] == "This is page 2"
    assert ocr.processed_pages == 2


@pytest.mark.usefixtures("mock_clean_conversation")
def test_clean_conversation(mocked_responses, api_client):
    convo_response = api_client.neural.clean_conversation(["abc123"])
    assert len(mocked_responses.calls) == 1
    request = mocked_responses.calls[0].request
    assert json.loads(request.body) == {"message_id": ["abc123"]}
    assert len(convo_response) == 1
    convo = convo_response[0]
    assert (
        convo.conversation
        == "<img src='cid:1781777f666586677621' /> This is the conversation"
    )
    assert convo.model_version == "0.0.1"


@pytest.mark.usefixtures("mock_clean_conversation")
def test_clean_conversation_options(mocked_responses, api_client):
    options = NeuralMessageOptions(False, False, False, False, False)
    api_client.neural.clean_conversation(["abc123"], options)
    request = mocked_responses.calls[0].request
    assert json.loads(request.body) == {
        "message_id": ["abc123"],
        "ignore_links": False,
        "ignore_images": False,
        "ignore_tables": False,
        "remove_conclusion_phrases": False,
        "images_as_markdowns": False,
    }


@pytest.mark.usefixtures("mock_clean_conversation")
def test_clean_conversation_extract_images(mocked_responses, api_client):
    convo = api_client.neural.clean_conversation(["abc123"])
    extracted_files = convo[0].extract_images()
    assert len(mocked_responses.calls) == 2
    assert len(extracted_files) == 1
    assert isinstance(extracted_files[0], File) is True
    assert extracted_files[0].id == "1781777f666586677621"

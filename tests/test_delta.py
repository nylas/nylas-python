import pytest
from urlobject import URLObject

from nylas.client.delta_models import Deltas, Delta
from nylas.client.restful_models import (
    Contact,
    File,
    Message,
    Draft,
    Thread,
    Event,
    Folder,
    Label,
)


@pytest.mark.usefixtures("mock_deltas_since")
def test_deltas_since(mocked_responses, api_client):
    deltas = api_client.deltas.since("cursor")
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/delta"
    assert URLObject(request.url).query_dict == {"cursor": "cursor"}
    assert request.method == "GET"
    assert isinstance(deltas, Deltas)
    assert deltas.cursor_start == "start_cursor"
    assert deltas.cursor_end == "end_cursor"
    assert len(deltas.deltas) == 8
    assert isinstance(deltas.deltas[0].attributes, Contact)
    assert deltas.deltas[0].cursor == "contact_cursor"
    assert deltas.deltas[0].event == "create"
    assert deltas.deltas[0].id == "delta-1"
    assert deltas.deltas[0].object == "contact"
    assert isinstance(deltas.deltas[1].attributes, File)
    assert deltas.deltas[1].cursor == "file_cursor"
    assert deltas.deltas[1].event == "create"
    assert deltas.deltas[1].id == "delta-2"
    assert deltas.deltas[1].object == "file"
    assert isinstance(deltas.deltas[2].attributes, Message)
    assert deltas.deltas[2].cursor == "message_cursor"
    assert deltas.deltas[2].event == "create"
    assert deltas.deltas[2].id == "delta-3"
    assert deltas.deltas[2].object == "message"
    assert isinstance(deltas.deltas[3].attributes, Draft)
    assert deltas.deltas[3].cursor == "draft_cursor"
    assert deltas.deltas[3].event == "create"
    assert deltas.deltas[3].id == "delta-4"
    assert deltas.deltas[3].object == "draft"
    assert isinstance(deltas.deltas[4].attributes, Thread)
    assert deltas.deltas[4].cursor == "thread_cursor"
    assert deltas.deltas[4].event == "create"
    assert deltas.deltas[4].id == "delta-5"
    assert deltas.deltas[4].object == "thread"
    assert isinstance(deltas.deltas[5].attributes, Event)
    assert deltas.deltas[5].cursor == "event_cursor"
    assert deltas.deltas[5].event == "create"
    assert deltas.deltas[5].id == "delta-6"
    assert deltas.deltas[5].object == "event"
    assert isinstance(deltas.deltas[6].attributes, Folder)
    assert deltas.deltas[6].cursor == "folder_cursor"
    assert deltas.deltas[6].event == "create"
    assert deltas.deltas[6].id == "delta-7"
    assert deltas.deltas[6].object == "folder"
    assert isinstance(deltas.deltas[7].attributes, Label)
    assert deltas.deltas[7].cursor == "label_cursor"
    assert deltas.deltas[7].event == "create"
    assert deltas.deltas[7].id == "delta-8"
    assert deltas.deltas[7].object == "label"


@pytest.mark.usefixtures("mock_delta_cursor")
def test_delta_cursor(mocked_responses, api_client):
    cursor = api_client.deltas.latest_cursor()
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/delta/latest_cursor"
    assert request.method == "POST"
    assert cursor == "cursor"


def evaluate_contact_delta(delta):
    assert isinstance(delta, Delta)
    assert isinstance(delta.attributes, Contact)
    assert delta.cursor == "contact_cursor"
    assert delta.event == "create"
    assert delta.id == "delta-1"
    assert delta.object == "contact"


@pytest.mark.usefixtures("mock_delta_stream")
def test_delta_streaming(mocked_responses, api_client):
    streaming = api_client.deltas.stream("cursor")
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/delta/streaming"
    assert URLObject(request.url).query_dict == {"cursor": "cursor"}
    assert request.method == "GET"
    assert len(streaming) == 1
    evaluate_contact_delta(streaming[0])


@pytest.mark.usefixtures("mock_delta_stream")
def test_delta_longpoll(mocked_responses, api_client):
    longpoll = api_client.deltas.longpoll("cursor", 30)
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/delta/longpoll"
    assert URLObject(request.url).query_dict == {"cursor": "cursor", "timeout": "30"}
    assert request.method == "GET"
    assert isinstance(longpoll, Deltas)
    assert longpoll.cursor_start == "start_cursor"
    assert longpoll.cursor_end == "end_cursor"
    assert len(longpoll.deltas) == 1
    evaluate_contact_delta(longpoll.deltas[0])


@pytest.mark.usefixtures("mock_delta_stream")
def test_delta_callback(mocked_responses, api_client):
    api_client.deltas.stream("cursor", callback=evaluate_contact_delta)


@pytest.mark.usefixtures("mock_delta_stream")
def test_delta_optional_params(mocked_responses, api_client):
    api_client.deltas.longpoll(
        "cursor", 30, view="expanded", include_types=["event", "file"]
    )
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/delta/longpoll"
    assert URLObject(request.url).query_dict == {
        "cursor": "cursor",
        "timeout": "30",
        "view": "expanded",
        "include_types": "event,file",
    }
    assert request.method == "GET"


@pytest.mark.usefixtures("mock_delta_stream")
def test_delta_type_string(mocked_responses, api_client):
    api_client.deltas.longpoll("cursor", 30, view="expanded", excluded_types="event")
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/delta/longpoll"
    assert URLObject(request.url).query_dict == {
        "cursor": "cursor",
        "timeout": "30",
        "view": "expanded",
        "excluded_types": "event",
    }
    assert request.method == "GET"


@pytest.mark.usefixtures("mock_delta_stream")
def test_delta_set_both_types_raise_error(api_client):
    with pytest.raises(ValueError) as excinfo:
        api_client.deltas.longpoll(
            "cursor",
            30,
            view="expanded",
            excluded_types="event",
            include_types="file",
        )
    assert "You cannot set both include_types and excluded_types" in str(excinfo)

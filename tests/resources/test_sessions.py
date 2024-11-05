from nylas.resources.scheduler import Sessions

from nylas.models.scheduler import Session

class TestSession:
  def test_session_deserialization(self):
    session_json = {
      "session_id": "session-id",
    }

    session = Session.from_dict(session_json)

    assert session.session_id == "session-id"

  def test_create_session(self, http_client_response):
    sessions = Sessions(http_client_response)
    request_body = {
      "configuration_id": "configuration-123",
      "time_to_live": 30
    }

    sessions.create(request_body)

    http_client_response._execute.assert_called_once_with(
      "POST",
      "/v3/scheduling/sessions",
      None,
      None,
      request_body,
      overrides=None,
    )

  def test_destroy_session(self, http_client_delete_response):
    sessions = Sessions(http_client_delete_response)

    sessions.destroy(session_id="session-123")

    http_client_delete_response._execute.assert_called_once_with(
      "DELETE",
      "/v3/scheduling/sessions/session-123",
      None,
      None,
      None,
      overrides=None,
    )
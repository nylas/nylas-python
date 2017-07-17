import pytest
import responses
from nylas.client.errors import InvalidRequestError


@responses.activate
@pytest.mark.usefixtures(
    "mock_draft_saved_response", "mock_draft_updated_response",
    "mock_draft_sent_response"
)
def test_save_send_draft(api_client):
    draft = api_client.drafts.create()
    draft.to = [{'name': 'My Friend', 'email': 'my.friend@example.com'}]
    draft.subject = "Here's an attachment"
    draft.body = "Cheers mate!"
    draft.save()

    draft.subject = "Stay polish, stay hungary"
    draft.save(random_query='true', param2='param')
    assert draft.subject == 'Update #2'

    msg = draft.send()
    assert msg['thread_id'] == 'clm33kapdxkposgltof845v9s'

    # Second time should throw an error
    with pytest.raises(InvalidRequestError):
        draft.send()

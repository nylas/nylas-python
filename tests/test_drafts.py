import pytest
from nylas.client.errors import InvalidRequestError

# pylint: disable=len-as-condition


@pytest.mark.usefixtures(
    "mock_draft_saved_response", "mock_draft_sent_response"
)
def test_save_send_draft(api_client):
    draft = api_client.drafts.create()
    draft.to = [{'name': 'My Friend', 'email': 'my.friend@example.com'}]
    draft.subject = "Here's an attachment"
    draft.body = "Cheers mate!"
    draft.save()

    draft.subject = "Stay polish, stay hungary"
    draft.save()
    assert draft.subject == "Stay polish, stay hungary"

    msg = draft.send()
    assert msg['thread_id'] == 'clm33kapdxkposgltof845v9s'

    # Second time should throw an error
    with pytest.raises(InvalidRequestError):
        draft.send()


@pytest.mark.usefixtures("mock_files")
def test_draft_attachment(api_client):
    draft = api_client.drafts.create()
    attachment = api_client.files.create()
    attachment.filename = "dummy"
    attachment.data = "data"

    assert len(draft.file_ids) == 0
    draft.attach(attachment)
    assert len(draft.file_ids) == 1
    assert attachment.id in draft.file_ids

    unattached = api_client.files.create()
    unattached.filename = "unattached"
    unattached.data = "foo"
    draft.detach(unattached)
    assert len(draft.file_ids) == 1
    assert attachment.id in draft.file_ids
    assert unattached.id not in draft.file_ids

    draft.detach(attachment)
    assert len(draft.file_ids) == 0


@pytest.mark.usefixtures(
    "mock_draft_saved_response", "mock_draft_deleted_response"
)
def test_delete_draft(api_client):
    draft = api_client.drafts.create()
    # Unsaved draft shouldn't throw an error on .delete(), but won't actually
    # delete anything.
    draft.delete()
    # Now save the draft...
    draft.save()
    # ... and delete it for real.
    draft.delete()


@pytest.mark.usefixtures("mock_draft_saved_response")
def test_draft_version(api_client):
    draft = api_client.drafts.create()
    assert 'version' not in draft
    draft.save()
    assert draft['version'] == 0
    draft.update()
    assert draft['version'] == 1
    draft.update()
    assert draft['version'] == 2

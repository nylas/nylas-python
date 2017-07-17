import pytest
import responses
from nylas.client.restful_models import Account, APIAccount


def test_create_account(api_client, monkeypatch):
    monkeypatch.setattr(api_client, "is_opensource_api", lambda: False)
    account = api_client.accounts.create()
    assert isinstance(account, Account)


def test_create_apiaccount(api_client, monkeypatch):
    monkeypatch.setattr(api_client, "is_opensource_api", lambda: True)
    account = api_client.accounts.create()
    assert isinstance(account, APIAccount)


def test_account_json(api_client, monkeypatch):
    monkeypatch.setattr(api_client, "is_opensource_api", lambda: False)
    account = api_client.accounts.create()
    result = account.as_json()
    assert isinstance(result, dict)


@responses.activate
@pytest.mark.usefixtures("mock_accounts", "mock_upgrade")
def test_account_upgrade(api_client, app_id):
    api_client.app_id = app_id
    account = api_client.accounts.first()
    assert account.billing_state == "trial"
    account = account.upgrade()
    assert account.billing_state == "paid"
    account = account.downgrade()
    assert account.billing_state == "trial"


def test_account_delete(api_client, monkeypatch):
    monkeypatch.setattr(api_client, "is_opensource_api", lambda: False)
    account = api_client.accounts.create()
    with pytest.raises(NotImplementedError):
        account.delete()

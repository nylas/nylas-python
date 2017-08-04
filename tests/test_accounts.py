import pytest
from nylas.client.restful_models import Account, APIAccount, SingletonAccount


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


@pytest.mark.usefixtures("mock_accounts", "mock_account_management")
def test_account_upgrade(api_client, app_id):
    api_client.app_id = app_id
    account = api_client.accounts.first()
    assert account.billing_state == "paid"
    account = account.downgrade()
    assert account.billing_state == "cancelled"
    account = account.upgrade()
    assert account.billing_state == "paid"


def test_account_delete(api_client, monkeypatch):
    monkeypatch.setattr(api_client, "is_opensource_api", lambda: False)
    account = api_client.accounts.create()
    with pytest.raises(NotImplementedError):
        account.delete()


@pytest.mark.usefixtures("mock_accounts", "mock_account")
def test_account_access(api_client):
    account1 = api_client.account
    assert isinstance(account1, SingletonAccount)
    account2 = api_client.accounts[0]
    assert isinstance(account2, APIAccount)
    account3 = api_client.accounts.first()
    assert isinstance(account3, APIAccount)
    assert account1.as_json() == account2.as_json() == account3.as_json()

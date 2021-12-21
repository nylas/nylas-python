from datetime import datetime
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


@pytest.mark.usefixtures("mock_ip_addresses")
def test_ip_addresses(api_client_with_client_id):
    result = api_client_with_client_id.ip_addresses()
    assert isinstance(result, dict)
    assert "updated_at" in result
    assert "ip_addresses" in result


@pytest.mark.usefixtures("mock_token_info", "mock_account")
def test_token_info(api_client_with_client_id):
    result = api_client_with_client_id.token_info()
    assert isinstance(result, dict)
    assert "updated_at" in result
    assert "scopes" in result


@pytest.mark.usefixtures("mock_account")
def test_account_datetime(api_client):
    account = api_client.account
    assert account.linked_at == datetime(2017, 7, 24, 18, 18, 19)


@pytest.mark.usefixtures("mock_accounts", "mock_account_management")
def test_account_upgrade(api_client, client_id):
    api_client.client_id = client_id
    account = api_client.accounts.first()
    assert account.billing_state == "paid"
    account = account.downgrade()
    assert account.billing_state == "cancelled"
    account = account.upgrade()
    assert account.billing_state == "paid"


@pytest.mark.usefixtures("mock_revoke_all_tokens", "mock_account")
def test_revoke_all_tokens(api_client_with_client_id):
    assert api_client_with_client_id.access_token is not None
    api_client_with_client_id.revoke_all_tokens()
    assert api_client_with_client_id.access_token is None


@pytest.mark.usefixtures("mock_revoke_all_tokens", "mock_account")
def test_revoke_all_tokens_with_keep_access_token(
    api_client_with_client_id, access_token
):
    assert api_client_with_client_id.access_token == access_token
    api_client_with_client_id.revoke_all_tokens(keep_access_token=access_token)
    assert api_client_with_client_id.access_token == access_token


@pytest.mark.usefixtures("mock_accounts", "mock_account")
def test_account_access(api_client):
    account1 = api_client.account
    assert isinstance(account1, SingletonAccount)
    account2 = api_client.accounts[0]
    assert isinstance(account2, APIAccount)
    account3 = api_client.accounts.first()
    assert isinstance(account3, APIAccount)
    assert account1.as_json() == account2.as_json() == account3.as_json()


@pytest.mark.usefixtures("mock_accounts")
def test_account_metadata(api_client_with_client_id, monkeypatch):
    monkeypatch.setattr(api_client_with_client_id, "is_opensource_api", lambda: False)
    account1 = api_client_with_client_id.accounts[0]
    account1["metadata"] = {"test": "value"}
    account1.save()
    assert account1["metadata"] == {"test": "value"}


@pytest.mark.usefixtures("mock_accounts")
def test_application_account_delete(api_client_with_client_id, monkeypatch):
    monkeypatch.setattr(api_client_with_client_id, "is_opensource_api", lambda: False)
    account1 = api_client_with_client_id.accounts[0]
    api_client_with_client_id.accounts.delete(account1.id)


@pytest.mark.usefixtures("mock_application_details")
def test_application_details(api_client_with_client_id, monkeypatch):
    monkeypatch.setattr(api_client_with_client_id, "is_opensource_api", lambda: False)
    app_data = api_client_with_client_id.application_details()
    assert app_data["application_name"] == "My New App Name"
    assert app_data["icon_url"] == "http://localhost:5555/icon.png"
    assert app_data["redirect_uris"] == [
        "http://localhost:5555/login_callback",
        "localhost",
        "https://customerA.myapplication.com/login_callback",
    ]


@pytest.mark.usefixtures("mock_application_details")
def test_update_application_details(api_client_with_client_id, monkeypatch):
    monkeypatch.setattr(api_client_with_client_id, "is_opensource_api", lambda: False)
    updated_data = api_client_with_client_id.update_application_details(
        application_name="New Name",
        icon_url="https://myurl.com/icon.png",
        redirect_uris=["https://redirect.com"],
    )
    assert updated_data["application_name"] == "New Name"
    assert updated_data["icon_url"] == "https://myurl.com/icon.png"
    assert updated_data["redirect_uris"] == [
        "https://redirect.com",
    ]

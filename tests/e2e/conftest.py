import os
from typing import Dict, List
from uuid import uuid4

import pytest

from nylas import Client


_API_KEY_ENV_VARS = ("NYLAS_E2E_API_KEY", "NYLAS_API_KEY")
_API_URI_ENV_VARS = ("NYLAS_E2E_API_URI", "NYLAS_API_URI")


def _first_env_value(keys: tuple) -> str:
    for key in keys:
        value = os.getenv(key)
        if value:
            return value
    return ""


def extract_list_items(response_data):
    """
    Normalize list endpoint response payloads across API shapes.
    """
    if isinstance(response_data, list):
        return response_data

    if isinstance(response_data, dict):
        items = response_data.get("items")
        if isinstance(items, list):
            return items

    return []


def raw_list_ids(client: Client, path: str, id_key: str = "id", query_params=None):
    json_response, _headers = client.http_client._execute(
        "GET",
        path,
        None,
        query_params or {"limit": 200},
        None,
    )
    response_data = json_response.get("data")
    items = extract_list_items(response_data)
    return {item.get(id_key) for item in items if isinstance(item, dict) and item.get(id_key)}


@pytest.fixture
def raw_list_ids_helper():
    return raw_list_ids


@pytest.fixture(scope="session")
def e2e_client() -> Client:
    api_key = _first_env_value(_API_KEY_ENV_VARS)
    if not api_key:
        pytest.skip(
            "E2E tests require NYLAS_E2E_API_KEY (or NYLAS_API_KEY) to be set."
        )

    api_uri = _first_env_value(_API_URI_ENV_VARS)
    timeout = int(os.getenv("NYLAS_E2E_TIMEOUT", "90"))
    if api_uri:
        return Client(api_key=api_key, api_uri=api_uri, timeout=timeout)
    return Client(api_key=api_key, timeout=timeout)


@pytest.fixture
def unique_name():
    def _build(prefix: str) -> str:
        return f"{prefix}-{uuid4().hex[:10]}"

    return _build


@pytest.fixture
def e2e_resource_registry(e2e_client):
    registry: Dict[str, List[str]] = {
        "policies": [],
        "rules": [],
        "lists": [],
    }
    yield registry

    for policy_id in reversed(registry["policies"]):
        try:
            e2e_client.policies.destroy(policy_id)
        except Exception:
            pass

    for rule_id in reversed(registry["rules"]):
        try:
            e2e_client.rules.destroy(rule_id)
        except Exception:
            pass

    for list_id in reversed(registry["lists"]):
        try:
            e2e_client.lists.destroy(list_id)
        except Exception:
            pass


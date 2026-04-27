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


@pytest.fixture
def paginated_list_contains_id():
    def _contains_id(list_method, resource_id: str, limit: int = 100, max_pages: int = 20) -> bool:
        next_cursor = None
        seen_cursors = set()

        for _ in range(max_pages):
            query_params = {"limit": limit}
            if next_cursor:
                query_params["page_token"] = next_cursor

            response = list_method(query_params=query_params)
            if any(item.id == resource_id for item in response.data if item and item.id):
                return True

            if not response.next_cursor or response.next_cursor in seen_cursors:
                return False

            seen_cursors.add(response.next_cursor)
            next_cursor = response.next_cursor

        return False

    return _contains_id


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


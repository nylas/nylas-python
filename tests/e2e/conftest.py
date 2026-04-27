import os
from typing import Dict, List
from uuid import uuid4

import pytest

from nylas import Client


_E2E_API_KEY_ENV = "NYLAS_E2E_API_KEY"
_E2E_API_URI_ENV = "NYLAS_E2E_API_URI"
_E2E_RUN_ENV = "NYLAS_E2E_RUN"


def _is_truthy(value: str) -> bool:
    return value.lower() in {"1", "true", "yes", "on"}


def pytest_addoption(parser):
    parser.addoption(
        "--run-e2e",
        action="store_true",
        default=False,
        help="Run live E2E tests that call Nylas APIs.",
    )


def pytest_collection_modifyitems(config, items):
    run_e2e = config.getoption("--run-e2e") or _is_truthy(os.getenv(_E2E_RUN_ENV, ""))
    if run_e2e:
        return

    skip_e2e = pytest.mark.skip(
        reason=(
            "E2E tests are opt-in. Set NYLAS_E2E_RUN=1 or pass --run-e2e to execute."
        )
    )
    for item in items:
        if "e2e" in item.keywords:
            item.add_marker(skip_e2e)


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
    api_key = os.getenv(_E2E_API_KEY_ENV, "")
    if not api_key:
        pytest.skip(
            "E2E tests require NYLAS_E2E_API_KEY to be set."
        )

    api_uri = os.getenv(_E2E_API_URI_ENV, "")
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


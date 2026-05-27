from unittest.mock import patch

from nylas.models.lists import ListItem, NylasList
from nylas.resources.lists import Lists


class TestLists:
    def test_list_deserialization(self):
        list_json = {
            "id": "list-123",
            "name": "Blocked domains",
            "description": "Known spam senders",
            "type": "domain",
            "items_count": 2,
            "application_id": "app-123",
            "organization_id": "org-123",
            "created_at": 1712450952,
            "updated_at": 1712451952,
        }

        nylas_list = NylasList.from_dict(list_json)

        assert nylas_list.id == "list-123"
        assert nylas_list.name == "Blocked domains"
        assert nylas_list.description == "Known spam senders"
        assert nylas_list.type == "domain"
        assert nylas_list.items_count == 2
        assert nylas_list.application_id == "app-123"
        assert nylas_list.organization_id == "org-123"
        assert nylas_list.created_at == 1712450952
        assert nylas_list.updated_at == 1712451952

    def test_list_item_deserialization(self):
        item_json = {
            "id": "item-123",
            "list_id": "list-123",
            "value": "spam-domain.com",
            "created_at": 1712450952,
        }

        item = ListItem.from_dict(item_json)

        assert item.id == "item-123"
        assert item.list_id == "list-123"
        assert item.value == "spam-domain.com"
        assert item.created_at == 1712450952

    def test_list_deserialization_with_minimal_fields(self):
        nylas_list = NylasList.from_dict({"id": "list-123"}, infer_missing=True)

        assert nylas_list.id == "list-123"
        assert nylas_list.name is None
        assert nylas_list.description is None
        assert nylas_list.type is None
        assert nylas_list.items_count is None

    def test_list_item_deserialization_with_minimal_fields(self):
        item = ListItem.from_dict({"id": "item-123"}, infer_missing=True)

        assert item.id == "item-123"
        assert item.list_id is None
        assert item.value is None
        assert item.created_at is None

    def test_list_lists(self, http_client_list_response):
        lists = Lists(http_client_list_response)

        lists.list()

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/lists", None, None, None, overrides=None
        )

    def test_list_lists_with_query_params(self, http_client_list_response):
        lists = Lists(http_client_list_response)

        lists.list(query_params={"limit": 10, "page_token": "cursor-token"})

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/lists",
            None,
            {"limit": 10, "page_token": "cursor-token"},
            None,
            overrides=None,
        )

    def test_create_list(self, http_client_response):
        lists = Lists(http_client_response)
        request_body = {
            "name": "Blocked domains",
            "description": "Known spam senders",
            "type": "domain",
        }

        lists.create(request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "POST", "/v3/lists", None, None, request_body, overrides=None
        )

    def test_create_list_with_overrides(self, http_client_response):
        lists = Lists(http_client_response)
        request_body = {"name": "Allowed domains", "type": "domain"}
        overrides = {"headers": {"X-Test": "value"}}

        lists.create(request_body=request_body, overrides=overrides)

        http_client_response._execute.assert_called_once_with(
            "POST", "/v3/lists", None, None, request_body, overrides=overrides
        )

    def test_find_list(self, http_client_response):
        lists = Lists(http_client_response)

        lists.find(list_id="list-123")

        http_client_response._execute.assert_called_once_with(
            "GET", "/v3/lists/list-123", None, None, None, overrides=None
        )

    def test_find_list_with_overrides(self, http_client_response):
        lists = Lists(http_client_response)
        overrides = {"headers": {"X-Test": "value"}}

        lists.find(list_id="list-123", overrides=overrides)

        http_client_response._execute.assert_called_once_with(
            "GET", "/v3/lists/list-123", None, None, None, overrides=overrides
        )

    def test_update_list(self, http_client_response):
        lists = Lists(http_client_response)
        request_body = {"name": "Updated blocked domains", "description": "Updated description"}

        lists.update(list_id="list-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "PUT", "/v3/lists/list-123", None, None, request_body, overrides=None
        )

    def test_update_list_with_overrides(self, http_client_response):
        lists = Lists(http_client_response)
        request_body = {"description": "Updated description"}
        overrides = {"headers": {"X-Test": "value"}, "timeout": 42}

        lists.update(list_id="list-123", request_body=request_body, overrides=overrides)

        http_client_response._execute.assert_called_once_with(
            "PUT", "/v3/lists/list-123", None, None, request_body, overrides=overrides
        )

    def test_destroy_list(self, http_client_delete_response):
        lists = Lists(http_client_delete_response)

        lists.destroy(list_id="list-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE", "/v3/lists/list-123", None, None, None, overrides=None
        )

    def test_destroy_list_with_overrides(self, http_client_delete_response):
        lists = Lists(http_client_delete_response)
        overrides = {"headers": {"X-Test": "value"}}

        lists.destroy(list_id="list-123", overrides=overrides)

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE", "/v3/lists/list-123", None, None, None, overrides=overrides
        )

    def test_list_items(self, http_client_list_response):
        lists = Lists(http_client_list_response)

        lists.list_items(list_id="list-123")

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/lists/list-123/items", None, None, None, overrides=None
        )

    def test_list_items_with_query_params(self, http_client_list_response):
        lists = Lists(http_client_list_response)

        lists.list_items(list_id="list-123", query_params={"limit": 50, "page_token": "next"})

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/lists/list-123/items",
            None,
            {"limit": 50, "page_token": "next"},
            None,
            overrides=None,
        )

    def test_list_items_with_overrides(self, http_client_list_response):
        lists = Lists(http_client_list_response)
        overrides = {"headers": {"X-Test": "value"}}

        lists.list_items(list_id="list-123", overrides=overrides)

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/lists/list-123/items",
            None,
            None,
            None,
            overrides=overrides,
        )

    def test_add_items(self, http_client_response):
        lists = Lists(http_client_response)
        request_body = {"items": ["spam-domain.com", "phishing-example.net"]}

        lists.add_items(list_id="list-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/lists/list-123/items",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_add_items_with_overrides(self, http_client_response):
        lists = Lists(http_client_response)
        request_body = {"items": ["trusted-domain.com"]}
        overrides = {"headers": {"X-Test": "value"}}

        lists.add_items(list_id="list-123", request_body=request_body, overrides=overrides)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/lists/list-123/items",
            None,
            None,
            request_body,
            overrides=overrides,
        )

    def test_remove_items(self, http_client_response):
        lists = Lists(http_client_response)
        request_body = {"items": ["spam-domain.com"]}

        lists.remove_items(list_id="list-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/lists/list-123/items",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_remove_items_with_overrides(self, http_client_response):
        lists = Lists(http_client_response)
        request_body = {"items": ["spam-domain.com"]}
        overrides = {"headers": {"X-Test": "value"}}

        lists.remove_items(list_id="list-123", request_body=request_body, overrides=overrides)

        http_client_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/lists/list-123/items",
            None,
            None,
            request_body,
            overrides=overrides,
        )

    def test_remove_items_deserializes_using_nylas_list(self, http_client):
        lists = Lists(http_client)
        request_body = {"items": ["spam-domain.com"]}
        http_client._execute = lambda *args, **kwargs: (
            {
                "request_id": "abc-123",
                "data": {
                    "id": "list-123",
                    "name": "Blocked domains",
                    "type": "domain",
                    "items_count": 0,
                },
            },
            {"X-Test-Header": "test"},
        )

        with patch("nylas.resources.lists.Response.from_dict") as response_from_dict:
            lists.remove_items(list_id="list-123", request_body=request_body)

        response_from_dict.assert_called_once_with(
            {
                "request_id": "abc-123",
                "data": {
                    "id": "list-123",
                    "name": "Blocked domains",
                    "type": "domain",
                    "items_count": 0,
                },
            },
            NylasList,
            {"X-Test-Header": "test"},
        )

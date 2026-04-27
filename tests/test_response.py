from nylas.models.response import ListResponse
from nylas.models.rules import Rule


class TestListResponse:
    def test_from_dict_with_list_data(self):
        response = {
            "request_id": "req-123",
            "data": [{"id": "rule-1", "name": "Rule One"}],
            "next_cursor": "cursor-1",
        }

        parsed = ListResponse.from_dict(response, Rule)

        assert parsed.request_id == "req-123"
        assert parsed.next_cursor == "cursor-1"
        assert len(parsed.data) == 1
        assert parsed.data[0].id == "rule-1"

    def test_from_dict_with_items_wrapper(self):
        response = {
            "request_id": "req-456",
            "data": {
                "items": [{"id": "rule-2", "name": "Rule Two"}],
                "next_cursor": "cursor-2",
            },
        }

        parsed = ListResponse.from_dict(response, Rule)

        assert parsed.request_id == "req-456"
        assert parsed.next_cursor == "cursor-2"
        assert len(parsed.data) == 1
        assert parsed.data[0].id == "rule-2"

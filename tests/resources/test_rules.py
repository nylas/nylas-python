from nylas.models.rules import Rule, RuleEvaluation
from nylas.resources.rules import Rules


class TestRules:
    def test_rule_deserialization(self, http_client):
        rule_json = {
            "id": "rule-123",
            "name": "Block spam senders",
            "description": "Marks mail from spam-domain.com as spam",
            "priority": 1,
            "enabled": True,
            "trigger": "inbound",
            "match": {
                "operator": "any",
                "conditions": [
                    {"field": "from.domain", "operator": "is", "value": "spam-domain.com"}
                ],
            },
            "actions": [{"type": "mark_as_spam"}],
            "application_id": "app-123",
            "organization_id": "org-123",
            "created_at": 1712450952,
            "updated_at": 1712450952,
        }

        rule = Rule.from_dict(rule_json)

        assert rule.id == "rule-123"
        assert rule.name == "Block spam senders"
        assert rule.description == "Marks mail from spam-domain.com as spam"
        assert rule.priority == 1
        assert rule.enabled is True
        assert rule.trigger == "inbound"
        assert rule.match is not None
        assert rule.match.operator == "any"
        assert rule.match.conditions is not None
        assert rule.match.conditions[0].field == "from.domain"
        assert rule.match.conditions[0].operator == "is"
        assert rule.match.conditions[0].value == "spam-domain.com"
        assert rule.actions is not None
        assert rule.actions[0].type == "mark_as_spam"
        assert rule.actions[0].value is None
        assert rule.application_id == "app-123"
        assert rule.organization_id == "org-123"
        assert rule.created_at == 1712450952
        assert rule.updated_at == 1712450952

    def test_rule_deserialization_with_minimal_fields(self, http_client):
        rule_json = {
            "id": "rule-123",
            "name": "Minimal rule",
        }

        rule = Rule.from_dict(rule_json, infer_missing=True)

        assert rule.id == "rule-123"
        assert rule.name == "Minimal rule"
        assert rule.description is None
        assert rule.match is None
        assert rule.actions is None
        assert rule.created_at is None
        assert rule.updated_at is None

    def test_rule_evaluation_deserialization(self, http_client):
        evaluation_json = {
            "id": "evaluation-123",
            "grant_id": "grant-123",
            "message_id": "message-123",
            "evaluated_at": 1712450952,
            "evaluation_stage": "inbox_processing",
            "evaluation_input": {
                "from_address": "spammer@spam-domain.com",
                "from_domain": "spam-domain.com",
                "from_tld": "com",
            },
            "applied_actions": {
                "marked_as_spam": True,
                "archived": True,
                "folder_ids": ["spam-folder"],
            },
            "matched_rule_ids": ["rule-123"],
            "application_id": "app-123",
            "organization_id": "org-123",
            "created_at": 1712450952,
            "updated_at": 1712450952,
        }

        evaluation = RuleEvaluation.from_dict(evaluation_json)

        assert evaluation.id == "evaluation-123"
        assert evaluation.grant_id == "grant-123"
        assert evaluation.message_id == "message-123"
        assert evaluation.evaluated_at == 1712450952
        assert evaluation.evaluation_stage == "inbox_processing"
        assert evaluation.evaluation_input is not None
        assert evaluation.evaluation_input.from_address == "spammer@spam-domain.com"
        assert evaluation.applied_actions is not None
        assert evaluation.applied_actions.marked_as_spam is True
        assert evaluation.applied_actions.archived is True
        assert evaluation.applied_actions.folder_ids == ["spam-folder"]
        assert evaluation.matched_rule_ids == ["rule-123"]
        assert evaluation.application_id == "app-123"
        assert evaluation.organization_id == "org-123"

    def test_rule_evaluation_deserialization_with_minimal_fields(self, http_client):
        evaluation_json = {
            "id": "evaluation-123",
            "grant_id": "grant-123",
        }

        evaluation = RuleEvaluation.from_dict(evaluation_json, infer_missing=True)

        assert evaluation.id == "evaluation-123"
        assert evaluation.grant_id == "grant-123"
        assert evaluation.message_id is None
        assert evaluation.evaluation_input is None
        assert evaluation.applied_actions is None
        assert evaluation.matched_rule_ids is None

    def test_list_rules(self, http_client_list_response):
        rules = Rules(http_client_list_response)

        rules.list()

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/rules", None, None, None, overrides=None
        )

    def test_list_rules_with_query_params(self, http_client_list_response):
        rules = Rules(http_client_list_response)

        rules.list(query_params={"limit": 10, "page_token": "next-page-token"})

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/rules",
            None,
            {"limit": 10, "page_token": "next-page-token"},
            None,
            overrides=None,
        )

    def test_create_rule(self, http_client_response):
        rules = Rules(http_client_response)
        request_body = {
            "name": "Block spam domains",
            "priority": 1,
            "trigger": "inbound",
            "match": {
                "operator": "any",
                "conditions": [
                    {"field": "from.domain", "operator": "is", "value": "spam-domain.com"}
                ],
            },
            "actions": [{"type": "block"}],
        }

        rules.create(request_body)

        http_client_response._execute.assert_called_once_with(
            "POST", "/v3/rules", None, None, request_body, overrides=None
        )

    def test_create_rule_with_overrides(self, http_client_response):
        rules = Rules(http_client_response)
        request_body = {
            "name": "Block spam domains",
            "match": {
                "conditions": [
                    {"field": "from.domain", "operator": "is", "value": "spam-domain.com"}
                ],
            },
            "actions": [{"type": "block"}],
        }
        overrides = {"headers": {"X-Test": "value"}}

        rules.create(request_body, overrides=overrides)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/rules",
            None,
            None,
            request_body,
            overrides=overrides,
        )

    def test_find_rule(self, http_client_response):
        rules = Rules(http_client_response)

        rules.find("rule-123")

        http_client_response._execute.assert_called_once_with(
            "GET", "/v3/rules/rule-123", None, None, None, overrides=None
        )

    def test_find_rule_with_overrides(self, http_client_response):
        rules = Rules(http_client_response)
        overrides = {"headers": {"X-Test": "value"}}

        rules.find("rule-123", overrides=overrides)

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/rules/rule-123",
            None,
            None,
            None,
            overrides=overrides,
        )

    def test_update_rule(self, http_client_response):
        rules = Rules(http_client_response)
        request_body = {
            "enabled": False,
            "actions": [{"type": "archive"}],
        }

        rules.update("rule-123", request_body)

        http_client_response._execute.assert_called_once_with(
            "PUT", "/v3/rules/rule-123", None, None, request_body, overrides=None
        )

    def test_update_rule_with_overrides(self, http_client_response):
        rules = Rules(http_client_response)
        request_body = {
            "enabled": False,
        }
        overrides = {"headers": {"X-Test": "value"}, "timeout": 42}

        rules.update("rule-123", request_body, overrides=overrides)

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/rules/rule-123",
            None,
            None,
            request_body,
            overrides=overrides,
        )

    def test_destroy_rule(self, http_client_delete_response):
        rules = Rules(http_client_delete_response)

        rules.destroy("rule-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE", "/v3/rules/rule-123", None, None, None, overrides=None
        )

    def test_destroy_rule_with_overrides(self, http_client_delete_response):
        rules = Rules(http_client_delete_response)
        overrides = {"headers": {"X-Test": "value"}}

        rules.destroy("rule-123", overrides=overrides)

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/rules/rule-123",
            None,
            None,
            None,
            overrides=overrides,
        )

    def test_list_rule_evaluations(self, http_client_list_response):
        rules = Rules(http_client_list_response)

        rules.list_evaluations("grant-123")

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/grants/grant-123/rule-evaluations", None, None, None, overrides=None
        )

    def test_list_rule_evaluations_with_query_params(self, http_client_list_response):
        rules = Rules(http_client_list_response)

        rules.list_evaluations(
            "grant-123", query_params={"limit": 5, "page_token": "cursor-token"}
        )

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/grant-123/rule-evaluations",
            None,
            {"limit": 5, "page_token": "cursor-token"},
            None,
            overrides=None,
        )

    def test_list_rule_evaluations_with_overrides(self, http_client_list_response):
        rules = Rules(http_client_list_response)
        overrides = {"headers": {"X-Test": "value"}}

        rules.list_evaluations("grant-123", overrides=overrides)

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/grant-123/rule-evaluations",
            None,
            None,
            None,
            overrides=overrides,
        )

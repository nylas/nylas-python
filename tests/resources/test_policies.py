from nylas.models.policies import Policy
from nylas.resources.policies import Policies


class TestPolicies:
    def test_policy_deserialization(self, http_client):
        policy_json = {
            "id": "policy-123",
            "name": "Standard Agent Account Policy",
            "application_id": "app-123",
            "organization_id": "org-123",
            "options": {
                "additional_folders": ["processed", "spam-review"],
                "use_cidr_aliasing": True,
            },
            "limits": {
                "limit_attachment_size_limit": 26214400,
                "limit_attachment_count_limit": 50,
                "limit_attachment_allowed_types": ["image/png", "application/pdf"],
                "limit_size_total_mime": 52428800,
                "limit_storage_total": 1073741824,
                "limit_count_daily_message_per_grant": 1000,
                "limit_inbox_retention_period": 365,
                "limit_spam_retention_period": 30,
            },
            "rules": ["rule-1", "rule-2"],
            "spam_detection": {
                "use_list_dnsbl": True,
                "use_header_anomaly_detection": True,
                "spam_sensitivity": 1.5,
            },
            "created_at": 1712450952,
            "updated_at": 1712450952,
        }

        policy = Policy.from_dict(policy_json)

        assert policy.id == "policy-123"
        assert policy.name == "Standard Agent Account Policy"
        assert policy.application_id == "app-123"
        assert policy.organization_id == "org-123"
        assert policy.options is not None
        assert policy.options.additional_folders == ["processed", "spam-review"]
        assert policy.options.use_cidr_aliasing is True
        assert policy.limits is not None
        assert policy.limits.limit_attachment_size_limit == 26214400
        assert policy.limits.limit_attachment_count_limit == 50
        assert policy.limits.limit_attachment_allowed_types == [
            "image/png",
            "application/pdf",
        ]
        assert policy.limits.limit_size_total_mime == 52428800
        assert policy.limits.limit_storage_total == 1073741824
        assert policy.limits.limit_count_daily_message_per_grant == 1000
        assert policy.limits.limit_inbox_retention_period == 365
        assert policy.limits.limit_spam_retention_period == 30
        assert policy.rules == ["rule-1", "rule-2"]
        assert policy.spam_detection is not None
        assert policy.spam_detection.use_list_dnsbl is True
        assert policy.spam_detection.use_header_anomaly_detection is True
        assert policy.spam_detection.spam_sensitivity == 1.5
        assert policy.created_at == 1712450952
        assert policy.updated_at == 1712450952

    def test_policy_deserialization_with_minimal_fields(self, http_client):
        policy_json = {
            "id": "policy-123",
            "name": "Minimal Policy",
            "application_id": "app-123",
            "organization_id": "org-123",
        }

        policy = Policy.from_dict(policy_json, infer_missing=True)

        assert policy.id == "policy-123"
        assert policy.name == "Minimal Policy"
        assert policy.application_id == "app-123"
        assert policy.organization_id == "org-123"
        assert policy.options is None
        assert policy.limits is None
        assert policy.rules is None
        assert policy.spam_detection is None
        assert policy.created_at is None
        assert policy.updated_at is None

    def test_list_policies(self, http_client_list_response):
        policies = Policies(http_client_list_response)

        policies.list()

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/policies", None, None, None, overrides=None
        )

    def test_list_policies_with_query_params(self, http_client_list_response):
        policies = Policies(http_client_list_response)

        policies.list(query_params={"limit": 10, "page_token": "next-page-token"})

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/policies",
            None,
            {"limit": 10, "page_token": "next-page-token"},
            None,
            overrides=None,
        )

    def test_list_policies_with_overrides(self, http_client_list_response):
        policies = Policies(http_client_list_response)
        overrides = {"headers": {"X-Test": "value"}, "timeout": 42}

        policies.list(overrides=overrides)

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/policies",
            None,
            None,
            None,
            overrides=overrides,
        )

    def test_create_policy(self, http_client_response):
        policies = Policies(http_client_response)
        request_body = {
            "name": "Standard Agent Account Policy",
            "spam_detection": {
                "use_list_dnsbl": True,
                "use_header_anomaly_detection": True,
                "spam_sensitivity": 1.5,
            },
            "limits": {
                "limit_attachment_size_limit": 26214400,
                "limit_attachment_count_limit": 50,
                "limit_inbox_retention_period": 365,
                "limit_spam_retention_period": 30,
            },
        }

        policies.create(request_body)

        http_client_response._execute.assert_called_once_with(
            "POST", "/v3/policies", None, None, request_body, overrides=None
        )

    def test_create_policy_with_overrides(self, http_client_response):
        policies = Policies(http_client_response)
        request_body = {"name": "Standard Agent Account Policy"}
        overrides = {"headers": {"X-Test": "value"}}

        policies.create(request_body, overrides=overrides)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/policies",
            None,
            None,
            request_body,
            overrides=overrides,
        )

    def test_find_policy(self, http_client_response):
        policies = Policies(http_client_response)

        policies.find("policy-123")

        http_client_response._execute.assert_called_once_with(
            "GET", "/v3/policies/policy-123", None, None, None, overrides=None
        )

    def test_find_policy_with_overrides(self, http_client_response):
        policies = Policies(http_client_response)
        overrides = {"headers": {"X-Test": "value"}}

        policies.find("policy-123", overrides=overrides)

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/policies/policy-123",
            None,
            None,
            None,
            overrides=overrides,
        )

    def test_update_policy(self, http_client_response):
        policies = Policies(http_client_response)
        request_body = {
            "name": "Updated Agent Policy",
            "rules": ["rule-1", "rule-2"],
        }

        policies.update("policy-123", request_body)

        http_client_response._execute.assert_called_once_with(
            "PUT", "/v3/policies/policy-123", None, None, request_body, overrides=None
        )

    def test_update_policy_with_overrides(self, http_client_response):
        policies = Policies(http_client_response)
        request_body = {"rules": ["rule-1"]}
        overrides = {"headers": {"X-Test": "value"}}

        policies.update("policy-123", request_body, overrides=overrides)

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/policies/policy-123",
            None,
            None,
            request_body,
            overrides=overrides,
        )

    def test_destroy_policy(self, http_client_delete_response):
        policies = Policies(http_client_delete_response)

        policies.destroy("policy-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE", "/v3/policies/policy-123", None, None, None, overrides=None
        )

    def test_destroy_policy_with_overrides(self, http_client_delete_response):
        policies = Policies(http_client_delete_response)
        overrides = {"headers": {"X-Test": "value"}}

        policies.destroy("policy-123", overrides=overrides)

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/policies/policy-123",
            None,
            None,
            None,
            overrides=overrides,
        )

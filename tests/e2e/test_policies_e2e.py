import pytest


@pytest.mark.e2e
def test_policies_lifecycle_with_rule_association_e2e(
    e2e_client, e2e_resource_registry, unique_name, raw_list_ids_helper
):
    rule_response = e2e_client.rules.create(
        {
            "name": unique_name("e2e-policy-rule"),
            "trigger": "inbound",
            "match": {
                "operator": "any",
                "conditions": [
                    {
                        "field": "from.domain",
                        "operator": "is",
                        "value": "example.com",
                    }
                ],
            },
            "actions": [{"type": "archive"}],
        }
    )
    created_rule = rule_response.data
    assert created_rule.id
    e2e_resource_registry["rules"].append(created_rule.id)

    policy_response = e2e_client.policies.create(
        {"name": unique_name("e2e-policy"), "rules": [created_rule.id]}
    )
    created_policy = policy_response.data
    assert created_policy.id
    e2e_resource_registry["policies"].append(created_policy.id)

    find_response = e2e_client.policies.find(created_policy.id)
    assert find_response.data.id == created_policy.id

    updated_name = unique_name("e2e-policy-updated")
    update_response = e2e_client.policies.update(
        created_policy.id,
        {
            "name": updated_name,
            "rules": [created_rule.id],
            "spam_detection": {
                "use_list_dnsbl": True,
                "use_header_anomaly_detection": True,
            },
        },
    )
    # Some policy update responses may omit id; verify canonical state by refetching.
    assert update_response.data.name == updated_name

    refetch_response = e2e_client.policies.find(created_policy.id)
    assert refetch_response.data.id == created_policy.id
    assert refetch_response.data.name == updated_name
    assert refetch_response.data.rules is not None
    assert created_rule.id in refetch_response.data.rules

    returned_policy_ids = raw_list_ids_helper(e2e_client, "/v3/policies")
    assert created_policy.id in returned_policy_ids

    destroy_policy_response = e2e_client.policies.destroy(created_policy.id)
    assert destroy_policy_response.request_id
    e2e_resource_registry["policies"].remove(created_policy.id)

    destroy_rule_response = e2e_client.rules.destroy(created_rule.id)
    assert destroy_rule_response.request_id
    e2e_resource_registry["rules"].remove(created_rule.id)


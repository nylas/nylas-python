import pytest


@pytest.mark.e2e
def test_rules_lifecycle_e2e(
    e2e_client, e2e_resource_registry, unique_name, paginated_list_contains_id
):
    create_response = e2e_client.rules.create(
        {
            "name": unique_name("e2e-rule"),
            "description": "Created by SDK e2e test",
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
    created_rule = create_response.data
    assert created_rule.id
    e2e_resource_registry["rules"].append(created_rule.id)

    find_response = e2e_client.rules.find(created_rule.id)
    assert find_response.data.id == created_rule.id

    updated_name = unique_name("e2e-rule-updated")
    update_response = e2e_client.rules.update(
        created_rule.id,
        {
            "name": updated_name,
            "enabled": False,
            "actions": [{"type": "mark_as_spam"}],
        },
    )
    assert update_response.data.id == created_rule.id
    assert update_response.data.name == updated_name

    assert paginated_list_contains_id(e2e_client.rules.list, created_rule.id)

    destroy_response = e2e_client.rules.destroy(created_rule.id)
    assert destroy_response.request_id
    e2e_resource_registry["rules"].remove(created_rule.id)


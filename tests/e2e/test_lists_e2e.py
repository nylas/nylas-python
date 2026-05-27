import pytest


@pytest.mark.e2e
def test_lists_lifecycle_e2e(e2e_client, e2e_resource_registry, unique_name):
    create_response = e2e_client.lists.create(
        {
            "name": unique_name("e2e-list"),
            "type": "domain",
            "description": "Created by SDK e2e test",
        }
    )
    created_list = create_response.data
    assert created_list.id
    assert created_list.type == "domain"
    e2e_resource_registry["lists"].append(created_list.id)

    found_response = e2e_client.lists.find(created_list.id)
    assert found_response.data.id == created_list.id

    updated_name = unique_name("e2e-list-updated")
    update_response = e2e_client.lists.update(
        created_list.id,
        {"name": updated_name, "description": "Updated by SDK e2e test"},
    )
    assert update_response.data.id == created_list.id
    assert update_response.data.name == updated_name

    first_domain = f"{unique_name('allowed')}.example"
    second_domain = f"{unique_name('blocked')}.example"
    add_items_response = e2e_client.lists.add_items(
        created_list.id, {"items": [first_domain, second_domain]}
    )
    assert add_items_response.data.id == created_list.id

    list_items_response = e2e_client.lists.list_items(
        created_list.id, query_params={"limit": 200}
    )
    item_values = {item.value for item in list_items_response.data if item.value}
    assert first_domain in item_values
    assert second_domain in item_values

    remove_items_response = e2e_client.lists.remove_items(
        created_list.id, {"items": [first_domain]}
    )
    assert remove_items_response.data.id == created_list.id

    after_remove_response = e2e_client.lists.list_items(
        created_list.id, query_params={"limit": 200}
    )
    item_values_after_remove = {
        item.value for item in after_remove_response.data if item.value
    }
    assert first_domain not in item_values_after_remove
    assert second_domain in item_values_after_remove

    destroy_response = e2e_client.lists.destroy(created_list.id)
    assert destroy_response.request_id
    e2e_resource_registry["lists"].remove(created_list.id)


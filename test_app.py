import requests
import os
import uuid

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def test_get_all_items():
    """GET request with no parameters returns appropriate response"""
    res = requests.get(f"{BASE_URL}/items")
    assert res.status_code == 200
    assert "data" in res.json()


def test_get_item_found():
    """GET request with appropriate parameters returns expected JSON from database"""
    test_item = {"name": "test_item", "description": "test description"}
    post_res = requests.post(f"{BASE_URL}/items", json=test_item)
    assert post_res.status_code == 201

    item_id = post_res.json()["data"]["id"]

    get_res = requests.get(f"{BASE_URL}/items/{item_id}")
    assert get_res.status_code == 200
    assert get_res.json()["data"]["name"] == "test_item"


def test_get_item_not_found():
    """GET request that finds no results returns appropriate response"""
    res = requests.get(f"{BASE_URL}/items/nonexistent-id")
    assert res.status_code == 404
    assert "Item not found" in res.json()["detail"]


def test_get_item_with_incorrect_parameters():
    """GET request with incorrect parameters returns appropriate response"""
    res = requests.get(f"{BASE_URL}/items/")
    assert res.status_code == 200


def test_post_creates_item():
    """POST request results in JSON body being stored in database and S3"""
    test_item = {
        "name": f"new_item_{uuid.uuid4()}",
        "value": 42,
        "tags": ["test", "item"],
    }
    res = requests.post(f"{BASE_URL}/items", json=test_item)

    assert res.status_code == 201
    response_data = res.json()["data"]
    assert "id" in response_data
    assert response_data["name"] == test_item["name"]
    assert response_data["value"] == 42


def test_post_empty_body():
    """POST request with empty body returns appropriate response"""
    res = requests.post(f"{BASE_URL}/items", json={})
    assert res.status_code == 201


def test_post_duplicate_item():
    """POST request with duplicate data returns appropriate response"""
    test_item = {"id": f"duplicate-test-{uuid.uuid4()}", "name": "duplicate_item"}

    res1 = requests.post(f"{BASE_URL}/items", json=test_item)
    assert res1.status_code == 201

    res2 = requests.post(f"{BASE_URL}/items", json=test_item)
    assert res2.status_code == 409
    assert "already exists" in res2.json()["detail"]


def test_put_updates_existing_item():
    """PUT request targeting existing resource updates database and S3"""
    test_item = {"name": "original_name", "value": 100}
    post_res = requests.post(f"{BASE_URL}/items", json=test_item)
    assert post_res.status_code == 201

    item_id = post_res.json()["data"]["id"]

    updated_item = {"name": "updated_name", "value": 200, "new_field": "added"}
    put_res = requests.put(f"{BASE_URL}/items/{item_id}", json=updated_item)

    assert put_res.status_code == 200
    response_data = put_res.json()["data"]
    assert response_data["name"] == "updated_name"
    assert response_data["value"] == 200
    assert response_data["new_field"] == "added"
    assert response_data["id"] == item_id


def test_put_nonexistent_item():
    """PUT request with no valid target returns appropriate response"""
    test_item = {"name": "test", "value": 123}
    res = requests.put(f"{BASE_URL}/items/nonexistent-id", json=test_item)

    assert res.status_code == 404
    assert "Item not found" in res.json()["detail"]


def test_delete_existing_item():
    """DELETE request removes item from database and S3"""
    test_item = {"name": "to_be_deleted", "value": 999}
    post_res = requests.post(f"{BASE_URL}/items", json=test_item)
    assert post_res.status_code == 201

    item_id = post_res.json()["data"]["id"]

    delete_res = requests.delete(f"{BASE_URL}/items/{item_id}")
    assert delete_res.status_code == 200
    assert "deleted successfully" in delete_res.json()["data"]["message"]

    get_res = requests.get(f"{BASE_URL}/items/{item_id}")
    assert get_res.status_code == 404


def test_delete_nonexistent_item():
    """DELETE request with no valid target returns appropriate response"""
    res = requests.delete(f"{BASE_URL}/items/nonexistent-id")

    assert res.status_code == 404
    assert "Item not found" in res.json()["detail"]


def test_delete_empty_id():
    """DELETE request with empty ID returns appropriate response"""
    res = requests.delete(f"{BASE_URL}/items/")
    assert res.status_code == 405  # Method not allowed for trailing slash


def test_full_crud_workflow():
    """Test complete create-read-update-delete workflow"""
    # Create
    item = {"name": f"workflow_test_{uuid.uuid4()}", "status": "active"}
    post_res = requests.post(f"{BASE_URL}/items", json=item)
    assert post_res.status_code == 201
    item_id = post_res.json()["data"]["id"]

    # Read
    get_res = requests.get(f"{BASE_URL}/items/{item_id}")
    assert get_res.status_code == 200
    assert get_res.json()["data"]["name"] == item["name"]

    # Update
    updated_item = {"name": f"workflow_updated_{uuid.uuid4()}", "status": "inactive"}
    put_res = requests.put(f"{BASE_URL}/items/{item_id}", json=updated_item)
    assert put_res.status_code == 200
    assert put_res.json()["data"]["name"] == updated_item["name"]

    # Delete
    delete_res = requests.delete(f"{BASE_URL}/items/{item_id}")
    assert delete_res.status_code == 200

    # Verify deletion
    final_get = requests.get(f"{BASE_URL}/items/{item_id}")
    assert final_get.status_code == 404

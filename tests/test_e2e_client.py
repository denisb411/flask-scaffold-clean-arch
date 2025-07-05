import uuid
import pytest
from app.config import db

def unique_email(prefix="test") -> str:
    return f"{prefix}-{uuid.uuid4().hex}@e2e.com"

def test_list_clients(client):
    client.post("/api/v1/clients/", json={
        "name": "User A", "email": unique_email("a"), "phone": "1111"
    })
    client.post("/api/v1/clients/", json={
        "name": "User B", "email": unique_email("b"), "phone": "2222"
    })

    res = client.get("/api/v1/clients/")
    assert res.status_code == 200
    assert isinstance(res.json, list)
    assert len(res.json) == 2

def test_create_and_get_client(client):
    email = unique_email("get")
    res = client.post("/api/v1/clients/", json={
        "name": "E2E Tester", "email": email, "phone": "123456"
    })
    assert res.status_code == 201
    cid = res.json["id"]

    get_res = client.get(f"/api/v1/clients/{cid}")
    assert get_res.status_code == 200
    assert get_res.json["email"] == email

def test_update_client(client):
    old_email = unique_email("old")
    new_email = unique_email("new")
    res = client.post("/api/v1/clients/", json={
        "name": "Old", "email": old_email, "phone": "0000"
    })
    cid = res.json["id"]
    update_res = client.put(f"/api/v1/clients/{cid}", json={
        "name": "Updated", "email": new_email, "phone": "9999"
    })
    assert update_res.status_code == 200
    assert update_res.json["email"] == new_email

def test_delete_client(client):
    email = unique_email("del")
    res = client.post("/api/v1/clients/", json={
        "name": "To Delete", "email": email, "phone": "0000"
    })
    cid = res.json["id"]
    delete_res = client.delete(f"/api/v1/clients/{cid}")
    assert delete_res.status_code == 200

    get_after = client.get(f"/api/v1/clients/{cid}")
    assert get_after.status_code == 404

def test_health_check(client):
    res = client.get("/health/")
    assert res.status_code == 200
    assert res.json == {"status": "healthy"}

def test_create_client_invalid_payload(client):
    res = client.post("/api/v1/clients/", json={"name": "Missing Email"})
    assert res.status_code == 400

def test_update_client_not_found(client):
    email = unique_email("ghost")
    res = client.put("/api/v1/clients/9999", json={
        "name": "Ghost", "email": email, "phone": "1234"
    })
    assert res.status_code == 404

def test_delete_client_not_found(client):
    res = client.delete("/api/v1/clients/9999")
    assert res.status_code == 404

def test_get_client_not_found(client):
    res = client.get("/api/v1/clients/9999")
    assert res.status_code == 404

def test_update_client_invalid_payload(client):
    email = unique_email("valid")
    res = client.post("/api/v1/clients/", json={
        "name": "Valid", "email": email, "phone": "0000"
    })
    cid = res.json["id"]

    bad_res = client.put(f"/api/v1/clients/{cid}", json={
        "name": "No Email"
    })
    assert bad_res.status_code == 400
    assert "error" in bad_res.json

def test_create_client_with_invalid_json_body(client):
    # Sending a raw string instead of a JSON object (dict)
    res = client.post("/api/v1/clients/", json="not a dict")
    assert res.status_code == 400
    assert "Invalid or missing JSON body" in res.json["error"]

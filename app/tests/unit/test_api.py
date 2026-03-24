"""Unit tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.src.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_readiness_check():
    response = client.get("/ready")
    assert response.status_code == 200


def test_status_endpoint():
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "uptime_seconds" in data
    assert data["uptime_seconds"] >= 0


def test_create_item():
    payload = {"name": "Test Widget", "description": "A test item", "price": 9.99}
    response = client.post("/api/v1/items", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Widget"
    assert data["price"] == 9.99
    assert "id" in data


def test_get_item():
    # Create first
    payload = {"name": "Gizmo", "price": 4.99}
    create_resp = client.post("/api/v1/items", json=payload)
    item_id = create_resp.json()["id"]

    # Then fetch
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Gizmo"


def test_get_item_not_found():
    response = client.get("/api/v1/items/99999")
    assert response.status_code == 404


def test_update_item():
    payload = {"name": "Original", "price": 1.00}
    item_id = client.post("/api/v1/items", json=payload).json()["id"]

    updated = {"name": "Updated", "price": 2.50}
    response = client.put(f"/api/v1/items/{item_id}", json=updated)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"
    assert response.json()["price"] == 2.50


def test_delete_item():
    payload = {"name": "ToDelete", "price": 0.01}
    item_id = client.post("/api/v1/items", json=payload).json()["id"]

    response = client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code == 204

    # Confirm gone
    assert client.get(f"/api/v1/items/{item_id}").status_code == 404


def test_list_items_returns_list():
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

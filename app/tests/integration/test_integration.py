"""Integration tests — require running services."""
import pytest
import os
from fastapi.testclient import TestClient
from app.src.main import app

client = TestClient(app)

# Skip if not in CI environment with real services
pytestmark = pytest.mark.skipif(
    os.getenv("DATABASE_URL") is None,
    reason="Integration tests require DATABASE_URL"
)


def test_full_item_lifecycle():
    """Create → Read → Update → Delete lifecycle."""
    # Create
    item = {"name": "Integration Item", "description": "Full lifecycle test", "price": 15.00}
    create_resp = client.post("/api/v1/items", json=item)
    assert create_resp.status_code == 201
    item_id = create_resp.json()["id"]

    # Read
    get_resp = client.get(f"/api/v1/items/{item_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Integration Item"

    # Update
    updated = {"name": "Updated Integration Item", "price": 20.00}
    put_resp = client.put(f"/api/v1/items/{item_id}", json=updated)
    assert put_resp.status_code == 200
    assert put_resp.json()["price"] == 20.00

    # Delete
    del_resp = client.delete(f"/api/v1/items/{item_id}")
    assert del_resp.status_code == 204

    # Verify deleted
    assert client.get(f"/api/v1/items/{item_id}").status_code == 404


def test_health_endpoint_with_db():
    """Health check should pass when DB is connected."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

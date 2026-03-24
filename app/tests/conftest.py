"""Shared test fixtures for the FastAPI application."""
import pytest
from fastapi.testclient import TestClient
from app.src.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_items():
    """Clear in-memory store between tests."""
    from app.src import api as api_module
    api_module._items.clear()
    api_module._next_id = 1
    yield
    api_module._items.clear()
    api_module._next_id = 1

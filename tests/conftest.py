import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture(scope="function")
def client():
    return TestClient(app)

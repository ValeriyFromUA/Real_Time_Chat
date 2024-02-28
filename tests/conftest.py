import pytest
from fastapi.testclient import TestClient
from chat.main import app


@pytest.fixture
def client():
    return TestClient(app)

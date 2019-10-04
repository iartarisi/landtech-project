import pytest
from landtech.web import app


@pytest.fixture
def client():
    return app.test_client()

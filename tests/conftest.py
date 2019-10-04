import pytest
from landtech.web import app, create_app


@pytest.fixture
def client():
    return app.test_client()

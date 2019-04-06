import pytest
from locations.app import application


@pytest.fixture
def app():
    return application

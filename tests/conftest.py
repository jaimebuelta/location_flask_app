import pytest
from locations.app import create_app


@pytest.fixture
def app():
    application = create_app()
    return application

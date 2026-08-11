import copy
import pytest
from starlette.testclient import TestClient
import src.app as app_module
from src.app import app

INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture
def client(monkeypatch):
    # Restore a clean copy of activities before each test
    monkeypatch.setattr(app_module, "activities", copy.deepcopy(INITIAL_ACTIVITIES))
    return TestClient(app)

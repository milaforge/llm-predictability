from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from main import app, llm

client = TestClient(app)


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"text": ""},
        {"text": "a" * 2001},
        {"text": 123},
    ],
)
def test_invalid_input(payload):
    response = client.post("/classify", json=payload)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "output",
    [
        "not json",
        "{}",
        '{"category": "unknown"}',
        '{"category": "bug", "extra": true}',
    ],
)
def test_invalid_llm_output(monkeypatch, output):
    mock = SimpleNamespace(message=SimpleNamespace(content=output))
    monkeypatch.setattr(llm, "chat", AsyncMock(return_value=mock))

    response = client.post("/classify", json={"text": "Login fails"})
    assert response.status_code == 502


def test_valid_llm_output(monkeypatch):
    mock = SimpleNamespace(message=SimpleNamespace(content='{"category": "bug"}'))
    monkeypatch.setattr(llm, "chat", AsyncMock(return_value=mock))

    response = client.post("/classify", json={"text": "Login fails"})
    assert response.json() == {"category": "bug"}

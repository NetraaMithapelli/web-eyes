import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

FIXTURES = Path(__file__).resolve().parents[2] / "shared" / "schemas" / "fixtures"
client = TestClient(app)


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_plan_accepts_fixture_and_returns_valid_plan():
    r = client.post("/plan", json=load("sanitized_context.example.json"))
    assert r.status_code == 200
    body = r.json()
    assert body["snapshot_id"] == "snap_001"
    assert body["actions"][0]["type"] == "click"


def test_plan_rejects_unknown_fields():
    bad = load("sanitized_context.example.json")
    bad["raw_email"] = "priya.sharma@gmail.com"  # a field that must never be sent
    assert client.post("/plan", json=bad).status_code == 422


def test_plan_rejects_malformed_input():
    assert client.post("/plan", json={"hello": "world"}).status_code == 422

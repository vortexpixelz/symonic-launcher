from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_valid_pattern_gets_field_and_proof_segments() -> None:
    response = client.post("/api/v1/mcore/validate-pattern", json={"pattern": "01"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["valid"] is True
    assert [segment["kind"] for segment in payload["segments"]] == ["field", "proof"]
    assert payload["data"]["total_weight"] == "S3"


def test_overflow_pattern_gets_a_cut_segment() -> None:
    response = client.post("/api/v1/mcore/validate-pattern", json={"pattern": "22"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "overflow"
    assert payload["valid"] is False
    assert payload["segments"][-1]["kind"] == "cut"
    assert payload["segments"][-1]["label"] == "CUT · OVERFLOW"


def test_openapi_contract_is_exposed() -> None:
    response = client.get("/api/v1/openapi.json")

    assert response.status_code == 200
    assert "/api/v1/mcore/validate-pattern" in response.json()["paths"]

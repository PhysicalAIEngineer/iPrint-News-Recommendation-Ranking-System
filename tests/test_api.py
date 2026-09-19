from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_recommend():
    response = client.post(
        "/recommend",
        json={"user_id": "u1", "top_k": 5, "category": "technology"},
    )
    assert response.status_code == 200
    assert len(response.json()["recommendations"]) == 5


def test_rank():
    response = client.post(
        "/rank",
        json=[
            {
                "article_id": "a",
                "title": "A",
                "score": 0.1,
                "model_version": "v1",
            },
            {
                "article_id": "b",
                "title": "B",
                "score": 0.9,
                "model_version": "v1",
            },
        ],
    )
    assert response.status_code == 200
    assert response.json()[0]["article_id"] == "b"

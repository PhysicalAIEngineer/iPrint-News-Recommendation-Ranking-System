from fastapi.testclient import TestClient
from api.main import app
client=TestClient(app)
def test_health():
 r=client.get("/health"); assert r.status_code==200; assert r.json()["status"]=="healthy"
def test_recommend():
 r=client.post("/recommend",json={"user_id":"u1","top_k":5,"category":"technology"})
 assert r.status_code==200 and len(r.json()["recommendations"])==5
def test_rank():
 r=client.post("/rank",json=[{"article_id":"a","title":"A","score":.1,"model_version":"v1"},{"article_id":"b","title":"B","score":.9,"model_version":"v1"}])
 assert r.status_code==200 and r.json()[0]["article_id"]=="b"
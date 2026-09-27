from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_recommendations_success():
    response = client.get("/recommendations/user123")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user123"
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0

def test_invalid_user_id():
    response = client.get("/recommendations/user_@#$")
    assert response.status_code == 400

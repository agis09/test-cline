import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search_endpoint():
    response = client.post("/search", json={"query": "test query"})
    assert response.status_code == 200
    assert "results" in response.json()
    assert "agent_name" in response.json()

def test_image_search_endpoint():
    response = client.post("/search", json={"query": "sports car", "image_url": "https://i.ytimg.com/vi/ik7goS1sFAM/maxresdefault.jpg"})
    assert response.status_code == 200
    assert "results" in response.json()
    assert "agent_name" in response.json()

def test_config_endpoint():
    response = client.post("/config", json={"name": "New Agent Name", "personality": "New Agent Personality"})
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Agent configuration updated successfully."

    response = client.post("/search", json={"query": "test query"})
    assert response.status_code == 200
    assert response.json()["agent_name"] == "New Agent Name"

def test_chat_endpoint():
    response = client.post("/chat", json={"message": "test message"})
    assert response.status_code == 200
    assert "response" in response.json()
    assert "agent_name" in response.json()

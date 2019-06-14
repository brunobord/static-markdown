import requests


def test_document_with_space():
    response = requests.get("http://127.0.0.1:8080/with%20space.html")
    assert response.status_code == 200
    assert response.content.startswith(b"I am with space")

import requests


def test_home():
    response = requests.get("http://127.0.0.1:8080/images/knight.png")
    assert response.status_code == 200

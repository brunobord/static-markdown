import requests


def test_normal_style(http_server):
    response = requests.get("http://127.0.0.1:8080/mdown-readme/")
    assert response.status_code == 200
    assert b"Custom style" not in response.content


def test_custom_style(http_server_custom_style):
    response = requests.get("http://127.0.0.1:8081/mdown-readme/")
    assert response.status_code == 200
    assert b"Custom style" in response.content

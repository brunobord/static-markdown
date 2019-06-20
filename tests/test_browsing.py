import requests


def test_document_with_space(http_server):
    response = requests.get("http://127.0.0.1:8080/with%20space.html")
    assert response.status_code == 200
    assert response.content.startswith(b"I am with space")


def test_image(http_server):
    response = requests.get("http://127.0.0.1:8080/images/knight.png")
    assert response.status_code == 200


def test_redirect_subdir(http_server):
    response = requests.get("http://127.0.0.1:8080/subdir", allow_redirects=False)
    assert response.status_code == 301
    headers = response.headers
    assert "Location" in headers
    assert headers["Location"] == "/subdir/"


def test_404(http_server):
    response = requests.get("http://127.0.0.1:8080/unknown.html")
    assert response.status_code == 404


def test_head(http_server):
    response_get = requests.get("http://127.0.0.1:8080/")
    assert response_get.status_code == 200
    headers_get = response_get.headers

    response_head = requests.head("http://127.0.0.1:8080/")
    assert response_head.status_code == 200
    headers_head = response_head.headers
    assert headers_head == headers_get

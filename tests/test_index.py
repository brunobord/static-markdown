import requests


def test_home():
    response = requests.get("http://127.0.0.1:8080/index.html")
    assert response.status_code == 200
    index_html = response.content
    response = requests.get("http://127.0.0.1:8080/")
    assert response.status_code == 200
    assert response.content == index_html


def test_subdir():
    response = requests.get("http://127.0.0.1:8080/subdir/index.html")
    assert response.status_code == 200
    index_html = response.content
    response = requests.get("http://127.0.0.1:8080/subdir/")
    assert response.status_code == 200
    assert response.content == index_html


def test_404():
    response = requests.get("http://127.0.0.1:8080/unknown.html")
    assert response.status_code == 404


def test_alternate_index():
    response = requests.get("http://127.0.0.1:8080/alternate-index/")
    assert response.status_code == 200
    index_html = response.content
    response = requests.get("http://127.0.0.1:8080/alternate-index/index.htm")
    assert response.status_code == 200
    assert response.content == index_html
    assert response.content == b"I am the alternate index\n"


def test_empty_404():
    response = requests.get("http://127.0.0.1:8080/empty/")
    assert response.status_code == 404

import requests


def test_index_mdown(http_server):
    response = requests.get("http://127.0.0.1:8080/mdown/index.md")
    assert response.status_code == 200
    assert response.content.startswith(b"<!DOCTYPE html>")
    # Don't get fooled by the content-type
    assert response.headers["Content-Type"] == "text/html"
    index_md_content = response.content

    response = requests.get("http://127.0.0.1:8080/mdown/")
    assert response.status_code == 200
    # Don't get fooled by the content-type
    assert response.headers["Content-Type"] == "text/html"
    assert response.content == index_md_content


def test_index_readme(http_server):
    response = requests.get("http://127.0.0.1:8080/mdown-readme/index.md")
    assert response.status_code == 404

    response = requests.get("http://127.0.0.1:8080/mdown-readme/README.md")
    assert response.status_code == 200
    assert response.content.startswith(b"<!DOCTYPE html>")
    # Don't get fooled by the content-type
    assert response.headers["Content-Type"] == "text/html"
    index_md_content = response.content

    response = requests.get("http://127.0.0.1:8080/mdown-readme/")
    assert response.status_code == 200
    # Don't get fooled by the content-type
    assert response.headers["Content-Type"] == "text/html"
    assert response.content == index_md_content

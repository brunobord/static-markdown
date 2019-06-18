import requests


def test_home(http_server):
    response = requests.get("http://127.0.0.1:8080/index.html")
    assert response.status_code == 200
    index_html = response.content
    response = requests.get("http://127.0.0.1:8080/")
    assert response.status_code == 200
    assert response.content == index_html


def test_subdir(http_server):
    response = requests.get("http://127.0.0.1:8080/subdir/index.html")
    assert response.status_code == 200
    index_html = response.content
    response = requests.get("http://127.0.0.1:8080/subdir/")
    assert response.status_code == 200
    assert response.content == index_html


def test_404(http_server):
    response = requests.get("http://127.0.0.1:8080/unknown.html")
    assert response.status_code == 404


def test_alternate_index(http_server):
    response = requests.get("http://127.0.0.1:8080/alternate-index/")
    assert response.status_code == 200
    index_html = response.content
    response = requests.get("http://127.0.0.1:8080/alternate-index/index.htm")
    assert response.status_code == 200
    assert response.content == index_html
    assert response.content == b"I am the alternate index\n"


def test_empty_404(http_server):
    response = requests.get("http://127.0.0.1:8080/empty/")
    assert response.status_code == 200


def test_dirlist(http_server):
    response = requests.get("http://127.0.0.1:8080/no-index/")
    assert response.status_code == 200
    content = response.content
    # Another Directory
    assert b'<a href="/no-index/subdir/">subdir/</a>' in content
    # Two files
    assert b'<a href="/no-index/file.html">file.html</a>' in content
    assert b'<a href="/no-index/other-file.html">other-file.html</a>' in content

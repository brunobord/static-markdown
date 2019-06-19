import requests

from static_markdown import __version__


def test_server_headers(http_server):
    response = requests.get("http://127.0.0.1:8080/")
    headers = response.headers
    assert headers["Server"] == f"Static-Markdown/{__version__}"

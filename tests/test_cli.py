from unittest.mock import MagicMock, patch

from static_markdown.server import main


def test_main_regular_call():
    with patch("argparse.ArgumentParser.parse_args") as argument_mock:
        argument_mock.return_value = MagicMock(version=False, root=".", port=9999)
        with patch("http.server.HTTPServer.serve_forever") as serve_mock:
            serve_mock.return_value = True
            main()
            serve_mock.assert_called_once()


def test_main_with_version():
    with patch("argparse.ArgumentParser.parse_args") as argument_mock:
        argument_mock.return_value = MagicMock(version=True, root=".", port=9999)
        with patch("http.server.HTTPServer.serve_forever") as serve_mock:
            serve_mock.return_value = True
            main()
            serve_mock.assert_not_called()

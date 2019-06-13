#!/usr/bin/env python3
import argparse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from os.path import abspath, isdir

from .document import Document, DocumentError
from .helpers import DEFAULT_MARKDOWN_TEMPLATE, cd


class Server(HTTPServer):
    def __init__(self, *args, **kwargs):
        self._root = kwargs.pop("root", ".")
        _template_handler = kwargs.pop("markdown_template", None)
        if _template_handler:
            self._markdown_template = _template_handler.read()
        else:
            self._markdown_template = DEFAULT_MARKDOWN_TEMPLATE
        super().__init__(*args, **kwargs)


class StaticMarkdownHandler(BaseHTTPRequestHandler):
    @property
    def root(self):
        if not hasattr(self, "_root"):
            self._root = getattr(self.server, "_root")
        return self._root

    @property
    def markdown_template(self):
        if not hasattr(self, "_markdown_template"):
            self._markdown_template = getattr(self.server, "_markdown_template")
        return self._markdown_template

    def do_GET(self):
        try:
            document = Document(self.root, self.path, self.markdown_template)
        except DocumentError as exc:
            self.send_error(exc.status_code, exc.message)
            return

        # Before sending the headers, send the response status
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Length", str(document.content_length))
        self.send_header("Content-type", document._type)
        self.send_header("Last-Modified", document.last_modified)
        # Ending headers here
        self.end_headers()

        self.wfile.write(document.content)


def port(number):
    """
    A port value is a number between 0 and 65535.
    """
    try:
        number = int(number)
    except ValueError:
        raise argparse.ArgumentTypeError("invalid int value: '{}'".format(number))
    if 0 <= number <= 65535:
        return number
    raise argparse.ArgumentTypeError("port must be 0-65535")


def serve(root, port=8080, markdown_template=None):
    root = abspath(root)
    if not isdir(root):
        print("Error: `{}` is not a directory".format(root))
        return

    print(
        "Serving `{root}`..."
        "\nGo to: {scheme}://127.0.0.1:{port}".format(
            scheme="http", root=root, port=port
        )
    )
    with cd(root):
        server_address = ("", port)
        httpd = Server(
            server_address,
            StaticMarkdownHandler,
            root=root,
            markdown_template=markdown_template,
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
    print("Bye...")


def main():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="Path to serve statically")
    parser.add_argument(
        "-p", "--port", type=port, default=8080, help="Port number (0-65535)"
    )
    parser.add_argument(
        "--markdown-template",
        default=None,
        type=argparse.FileType("r"),
        help="Path to an alternate HTML template for Markdown files",
    )

    args = parser.parse_args()
    serve(root=args.root, port=args.port, markdown_template=args.markdown_template)


if __name__ == "__main__":
    main()
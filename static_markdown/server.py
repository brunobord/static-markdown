#!/usr/bin/env python3
import argparse
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from os.path import abspath, isdir

from loguru import logger

from . import __version__
from .document import Document, DocumentError, RedirectionException
from .helpers import DEFAULT_MARKDOWN_STYLE, DEFAULT_MARKDOWN_TEMPLATE, cd

log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
    "| <level>{level: <8}</level> | <level>{message}</level>"
)

logger.configure(
    handlers=[{"sink": sys.stderr, "format": log_format}],
    extra={"reqid": "-", "ip": "-", "user": "-"},
)


class Server(HTTPServer):
    def __init__(self, *args, **kwargs):
        self._root = kwargs.pop("root", ".")
        self._root_url = kwargs.pop("root_url", ".")
        stylesheet = kwargs.pop("stylesheet", None)

        # Default style
        self._style = DEFAULT_MARKDOWN_STYLE
        if stylesheet:
            self._style = stylesheet.read()

        # Template Handling
        _template_handler = kwargs.pop("markdown_template", None)
        if _template_handler:
            self._markdown_template = _template_handler.read()
        else:
            self._markdown_template = DEFAULT_MARKDOWN_TEMPLATE
        super().__init__(*args, **kwargs)


class StaticMarkdownHandler(BaseHTTPRequestHandler):
    server_version = "Static-Markdown/" + __version__

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

    @property
    def style(self):
        if not hasattr(self, "_style"):
            self._style = getattr(self.server, "_style")
        return self._style

    def get_document(self):
        """
        Return the appropriate document corresponding to the path.
        """
        try:
            document = Document(
                self.root, self.path, self.markdown_template, self.style
            )
        except DocumentError as exc:
            self.send_error(exc.status_code, exc.message)
            return
        except RedirectionException as exc:
            self.send_response(HTTPStatus.MOVED_PERMANENTLY)
            self.send_header("Location", f"{exc.location}")
            self.end_headers()
            return

        # Before sending the headers, send the response status
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Length", str(document.content_length))
        self.send_header("Content-type", document._type)
        self.send_header("Last-Modified", document.last_modified)
        # Ending headers here
        self.end_headers()
        return document

    def do_HEAD(self):
        """
        Handle HEAD requests
        """
        self.get_document()

    def do_GET(self):
        """
        Handle GET requests
        """
        document = self.get_document()
        if document:
            self.wfile.write(document.content)

    def _do_405(self):
        """
        Handle POST/PUT/PATCH/DELETE requests. Return 405.
        """
        self.send_response(HTTPStatus.METHOD_NOT_ALLOWED)
        self.end_headers()
        return

    do_PUT = do_DELETE = do_PATCH = do_POST = _do_405

    def log_message(self, format, *args):
        """
        Log handling
        """
        logger.info("%s - %s" % (self.address_string(), format % args))

    def log_error(self, format, *args):
        """
        Error log handling
        """
        logger.error("%s - %s" % (self.address_string(), format % args))

    def version_string(self):
        """
        Return the server software version string.
        """
        return self.server_version


def serve(root, port=8080, markdown_template=None, scheme="http", stylesheet=None):
    root = abspath(root)
    if not isdir(root):
        logger.error("Error: `{}` is not a directory".format(root))
        return

    root_url = f"{scheme}://127.0.0.1:{port}"
    logger.info(f"Serving `{root}`..." f"\nGo to: {root_url}")
    with cd(root):
        server_address = ("", port)
        httpd = Server(
            server_address,
            StaticMarkdownHandler,
            root=root,
            markdown_template=markdown_template,
            root_url=root_url,
            stylesheet=stylesheet,
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
    logger.info("Bye...")


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


def main():
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
    parser.add_argument(
        "--stylesheet",
        default=None,
        type=argparse.FileType("r"),
        help="Path to a custom stylesheet",
    )
    parser.add_argument(
        "--version", action="store_true", default=False, help="Return version and exit"
    )
    args = parser.parse_args()
    if args.version:
        print(f"Static Markdown v{__version__}")
        return
    serve(
        root=args.root,
        port=args.port,
        markdown_template=args.markdown_template,
        stylesheet=args.stylesheet,
    )

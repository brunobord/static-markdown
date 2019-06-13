import mimetypes
import os
from os.path import basename, isdir, isfile, join, splitext

import markdown
from markdown.extensions.toc import TocExtension
from mdx_gfm import GithubFlavoredMarkdownExtension
from slugify import slugify

from .helpers import DEFAULT_MARKDOWN_STYLE, date_time_string


def convert_md_source(source):
    "Convert Markdown content into HTML"
    html = markdown.markdown(
        source,
        extensions=[
            GithubFlavoredMarkdownExtension(),
            TocExtension(permalink=False, slugify=slugify),
        ],
    )
    return html


class DocumentError(Exception):
    """
    Error on the document
    """

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class Document(object):
    def __init__(self, root, path, markdown_template=None):
        # Init
        self.content_length = 0
        self.last_modified = None

        # Seek and load
        self.root = root
        self.path = path
        self.markdown_template = markdown_template
        self.filepath = self.get_filepath()
        self._type = self.guess_type()
        self.content = self.get_content()

    def guess_type(self):
        """
        Guess and return type
        """
        # split extension
        _, extension = splitext(self.filepath)
        if extension in (".md", ".markdown", ".mdown"):
            _type = "text/markdown"
        else:
            _type, encoding = mimetypes.guess_type(self.filepath, strict=False)
        return _type or "text/plain"

    def find_index(self, path):
        """
        Find the proper index in the directory
        """
        indexes = ("index.html", "index.htm", "index.md", "README.md", "readme.md")
        temp_path = self.root + path
        if path == "/" or isdir(temp_path):
            for index in indexes:
                index_path = join(temp_path, index)
                if isfile(index_path):
                    return index_path

    def get_filepath(self):
        index = self.find_index(self.path)
        if index:
            return index

        filepath = self.root + self.path
        if isfile(filepath):
            return filepath
        elif isdir(filepath):
            raise DocumentError(404, "Index not found, dirlist")
        raise DocumentError(404, "File Not Found")

    def get_content_markdown(self):
        """
        Load Markdown content and render it
        """
        with open(self.filepath, "r") as fh:
            mdown_content = fh.read()
            fs = os.fstat(fh.fileno())
        content = convert_md_source(mdown_content)
        # Render in template
        content = self.markdown_template.format(
            title=basename(self.filepath), style=DEFAULT_MARKDOWN_STYLE, content=content
        )
        self.content_length = len(content)
        self.last_modified = date_time_string(fs.st_mtime)
        # Somehow change the type, since we're rendering this as HTML
        self._type = "text/html"
        return content.encode()

    def get_content(self):
        """
        Return the (binary) content to stream to the HTTP client.
        """
        if self._type == "text/markdown":
            return self.get_content_markdown()

        try:
            fh = open(self.filepath, "rb")
            content = fh.read()
            fs = os.fstat(fh.fileno())
        except OSError:
            raise DocumentError(404, "File Not Found or I/O Error")
        finally:
            # Close file handler
            fh.close()
        # retrieve content length & last modified time.
        self.content_length = fs[6]
        self.last_modified = date_time_string(fs.st_mtime)
        # Return file content
        return content

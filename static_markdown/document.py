import mimetypes
import os
from os.path import basename, isdir, isfile, join, splitext

import markdown
from markdown.extensions.toc import TocExtension
from mdx_gfm import GithubFlavoredMarkdownExtension
from slugify import slugify

from .helpers import DEFAULT_MARKDOWN_STYLE, date_time_string, normalize_path


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
        self.path = normalize_path(path)
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
        """
        Return the filepath on the filesystem.
        """
        index = self.find_index(self.path)
        if index:
            return index

        filepath = self.root + self.path
        if isfile(filepath) or isdir(filepath):
            return filepath
        raise DocumentError(404, "File Not Found")

    def get_dirlist(self):
        content = []
        content.append(f"# Directory listing for {self.path}")
        path = self.path
        if not path.endswith("/"):
            path = path + "/"
        for name in os.listdir(self.filepath):
            fullpath = join(self.filepath, name)
            if isdir(fullpath):
                content.append(f"* [{name}/]({path}{name}/)")
            if isfile(fullpath):
                content.append(f"* [{name}]({path}{name})")
        content = "\n".join(content)
        return self.render_markdown(content)

    def render_markdown(self, mdown_content):
        # Markdown to HTML
        content = convert_md_source(mdown_content)
        # Render in template
        content = self.markdown_template.format(
            title=basename(self.filepath), style=DEFAULT_MARKDOWN_STYLE, content=content
        )
        self.content_length = len(content)
        self.last_modified = date_time_string(os.path.getmtime(self.filepath))
        # Somehow change the type, since we're rendering this as HTML
        self._type = "text/html"
        return content.encode()

    def get_content_markdown(self):
        """
        Load Markdown content and render it
        """
        with open(self.filepath, "r") as fh:
            mdown_content = fh.read()
        return self.render_markdown(mdown_content)

    def get_content(self):
        """
        Return the (binary) content to stream to the HTTP client.
        """
        if self._type == "text/markdown":
            return self.get_content_markdown()

        if isdir(self.filepath):
            return self.get_dirlist()

        try:
            fh = open(self.filepath, "rb")
            content = fh.read()
        except OSError:
            raise DocumentError(404, "File Not Found or I/O Error")
        finally:
            # Close file handler
            fh.close()
        # retrieve content length & last modified time.
        self.content_length = len(content)
        self.last_modified = date_time_string(os.path.getmtime(self.filepath))
        # Return file content
        return content

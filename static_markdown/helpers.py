import email
import posixpath
import time
import urllib.parse
from contextlib import contextmanager
from os import chdir, getcwd

DEFAULT_MARKDOWN_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<meta http-equiv="X-UA-Compatible" content="chrome=1">
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<style>
{style}
</style>
</head>
<body>
    <main>{content}</main>
</body>
</html>
"""

DEFAULT_MARKDOWN_STYLE = """
body { font-family: Helvetica, arial, freesans, clean, sans-serif; }
main { max-width: 70ch; padding: 2ch; margin: auto; }
code { font-family: monospace;}
"""


@contextmanager
def cd(dirname):
    """
    Context manager to temporarily change current directory.
    """
    _curdir = getcwd()
    chdir(dirname)
    yield
    chdir(_curdir)


def date_time_string(timestamp=None):
    """Return the current date and time formatted for a message header."""
    if timestamp is None:
        timestamp = time.time()
    return email.utils.formatdate(timestamp, usegmt=True)


def normalize_path(path):
    """
    Return URL-entity-free pathname
    """
    try:
        path = urllib.parse.unquote(path, errors="surrogatepass")
    except UnicodeDecodeError:
        path = urllib.parse.unquote(path)
    path = posixpath.normpath(path)
    return path

# Static Markdown

A static web server with markdown rendering feature.

It serves regular HTTP content (HTML, JS, CSS, images, etc), but when you're browsing a ``.md``, ``.mdown`` or ``.markdown`` file, it's converted into HTML and rendered as a (hopefully) readable page.

## IMPORTANT WARNING

**This server is not recommended for production. It's a toy to serve static files and Markdown content, but there's no guarantee about security, performance, availability, etc.**

## Installation

### via PyPI

Install this tool using pip to download it [from PyPI](https://pypi.org/project/static-markdown/). You may prefer to use a virtualenv, but you may also want to install "user-wide".

```shell
pip install static-markdown
pip install --user static-markdown
```

### Using the source

We're advising you to use ``virtualenv`` to install this package. Clone this repository, and, inside your *virtualenv*, run the following:

```shell
pip install -e ./
```

## Usage

Once it's installed, you can just change your current shell session to the designated directory and run the following:

```shell
cd /path/to/directory
serve-md
```

Alternatively, you can also run this command line from anywhere, but set the target path as a command argument:

```shell
serve-md /path/to/directory
```

Using these default option, you can now browse your "static website" by pointing your browser to: <http://127.0.0.1:8080/>.

Stop the server with Ctrl-C.

### Options

```
usage: serve-md [-h] [-p PORT] [--markdown-template MARKDOWN_TEMPLATE] [root]

positional arguments:
  root                  Path to serve statically

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port number (0-65535)
  --markdown-template MARKDOWN_TEMPLATE
                        Path to an alternate HTML template for Markdown files
```

### Browsing

Let's consider the following path tree:

```
.
├── empty
├── images
│   └── knight.png
├── index.html
├── mdown
│   └── index.md
├── mdown-readme
│   └── README.md
└── subdir
    └── index.html
```

Here is a table describing the different pages rendered with the given URL in your browser

| URL                | Content                | Content type | Status Code           |
|:-------------------|:-----------------------|:-------------|:----------------------|
| /                  | index.html             | text/html    | 200 OK                |
| /empty             | directory listing      | text/html    | 200 OK                |
| /images/knight.png | knight.png (as binary) | image/png    | 200 OK                |
| /mdown/            | index.md (as HTML)     | text/html    | 200 OK                |
| /mdown/index.md    | index.md (as HTML)     | text/html    | 200 OK                |
| /mdown-readme      | README.md (as HTML)    | text/html    | 200 OK                |
| /subdir            | redirect to /subdir/   | -            | 301 MOVED PERMANENTLY |
| /subdir/           | subdir/index.html      | text/html    | 200 OK                |

### Indexes

When browsing a directory, ``serve-md`` will look after the following files, in that specific order: "index.html", "index.htm", "index.md", "README.md", "readme.md". The first one of them to be found will be served as the index page of the directory.

If none of them is found, ``serve-md`` will return a directory listing. If you're using the "Markdown template" feature, it'll be used when rendering this page.

### Markdown templates

By default, Markdown files will be rendered as HTML using a minimal CSS. Using the ``--markdown-template`` option, you can use your own HTML template with a custom CSS to render generate the ``text/html``. You can find various examples in the ``example-options`` directory in the source repository.

We've used various minimalist CSS frameworks for rendering and layout:

* [miligram](https://milligram.io/),
* [mini css](https://minicss.org/),
* [Github Markdown CSS](https://github.com/sindresorhus/github-markdown-css),

## Hack

1. Clone this repository.
2. Write tests.
3. Implement stuff.
4. Open a Pull Request.

*Note:* I'm afraid that testing is a bit awkward right now, you'll have to open two shell sessions. In the first one, run this:

```shell
make serve
```

In the other one, run tests with:

```shell
make test
```

Your tests will hit the launched server that serves the ``example`` directory.

**Important:** Each time you're modifying any line of the server's code, you **HAVE** to stop and restart the server.

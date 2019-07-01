# Changelog

## master (unreleased)

* Added HEAD implementation (#7).
* Document and make sure that the POST, PUT, DELETE and PATCH verbs would return a 405 error.
* Default style: limit ``<img>`` width up to the page width.

## v0.2.0 (2019-06-19)

### New features

* Enabled directory listing.
* Redirect to URL with trailing slash when pointing at a directory (#4).
* A better logging using loguru.
* A better way to test the application, without having to start the server in another shell.
* Implement version handling via a ``__version__`` module property.
* Added server name and version in the returned Server headers (#6).

### Fixes & other changes

* Fix 404 error when trying to browse file with spaces in their names (#1).
* Readme instructions to install from PyPI.
* Document the fact that the server is not production-ready (#5).
* Added twine in extra requirements (dev).
* Added travis support for CI.

## v0.1.0 (2019-06-13)

Initial release.

* Statically serve your local directory,
* Render Markdown as HTML,
* Searching for an index (HTML or Markdown) when trying to browse a directory,
* Customize Markdown HTML rendering using a custom HTML template.

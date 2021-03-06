# Changelog

## master (unreleased)

Nothing here yet.

## v0.4.0 (2021-05-10)

### New features

* Add/Confirm Python 3.8 compatibility (#10).
* Add/Confirm Python 3.9 compatibility (#11).

### Other improvements & fixes

* Fixed CI & solved regressions by upgrading of `pytest-xprocess` & `Markdown` libraries.
* Added the compatibility badges - courtesy of shields.io (#15).
* Added the Travis CI badge - also switched from travis-ci.org to the .com instance, hopefully more future-proof (#17).

## v0.3.0 (2019-10-05)

### New features

* Added HEAD implementation (#7).
* Document and make sure that the POST, PUT, DELETE and PATCH verbs would return a 405 error.
* Enable using a custom stylesheet.

### Other improvements

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

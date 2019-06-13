PYTHON=python3
VENV=venv/bin/
DIRECTORY=example/

# Serve the example directory
serve: venv/bin/serve-md
	$(VENV)serve-md $(DIRECTORY)

# Run tests
test: venv/bin/serve-md
	$(VENV)tox

# Lint source files
lint: venv/bin/serve-md
	$(VENV)isort static_markdown/* tests/*
	$(VENV)black static_markdown/* tests/*

venv/bin/serve-md:
	virtualenv venv --python=$(PYTHON)
	$(VENV)pip install -e .[dev]

# Install dev environment
install-dev: venv/bin/serve-md

# Clean test/venv files and directories
clean:
	rm -Rf venv/ .tox/ build/

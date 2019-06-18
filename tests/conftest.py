from os.path import abspath, dirname, join

import pytest
from xprocess import ProcessStarter

current_dir = dirname(__file__)
project_dir = abspath(join(current_dir, ".."))
executable_dir = abspath(join(project_dir, "static_markdown"))
example_dir = abspath(join(project_dir, "example"))


@pytest.fixture
def http_server(xprocess):
    class Starter(ProcessStarter):
        pattern = "Serving"
        args = ["python", f"{executable_dir}/cli.py", example_dir]

    server = xprocess.ensure("server", Starter)
    return server

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

    _ = xprocess.ensure("server-default", Starter)
    info = xprocess.getinfo("server-default")
    assert info.isrunning()
    yield info
    xprocess.getinfo("server-default").terminate()


@pytest.fixture
def http_server_custom_style(xprocess):
    class Starter(ProcessStarter):
        pattern = "Serving"
        args = [
            "python",
            f"{executable_dir}/cli.py",
            example_dir,
            "--stylesheet",
            f"{example_dir}/style.css",
            "--port",
            "8081",
        ]

    _ = xprocess.ensure("server-custom-css", Starter)
    info = xprocess.getinfo("server-custom-css")
    assert info.isrunning()
    yield info
    xprocess.getinfo("server-custom-css").terminate()

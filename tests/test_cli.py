from click.testing import CliRunner
from campbellcontrol.cli import cli


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert "Show this message and exit" in result.output

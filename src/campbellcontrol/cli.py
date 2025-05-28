import click

import campbellcontrol.commands.commands as commands
from campbellcontrol.config import load_config
from campbellcontrol.connection.aws import AWSConnection
from campbellcontrol.control import AWSCommandHandler


class CommandContext:
    """Create one context object that holds a CommandHandler
    and the rest of the config - click may have a better way!"""

    def __init__(self, config: dict):
        # TODO - factory for loading the right broker, assume AWS now
        # https://github.com/NERC-CEH/campbell-mqtt-control/issues/14
        self.client = AWSConnection("cliclient", config["server"], config["port"])
        self.command_handler = AWSCommandHandler(self.client)
        self.config = config


@click.group(context_settings={"auto_envvar_prefix": "MQTT"})  # this allows for environment variables
@click.option("--config", default="config.yaml", type=click.Path())
@click.pass_context
def cli(ctx: click.Context, config: str) -> None:
    options = load_config(config)
    ctx.obj = CommandContext(options)


@cli.command()
@click.pass_obj
def ls(ctx: CommandContext) -> None:
    config = ctx.config
    command = commands.ListFiles(config["topic"], config["serial"], options={"response_suffix": "list"})
    # TODO wire up the command handler properly
    try:
        response = ctx.command_handler.send_command(command)
    except ConnectionError as err:
        click.echo(f"Could not connect to {config['server']}")
        click.echo(err)
        return

    if response is None:
        click.echo(f"Sorry, I couldn't connect to {config['serial']}")
        return

    if response["success"]:
        click.echo(f"Files on device {config['serial']}")
        for f in response["payload"]["fileList"]:
            click.echo(f)

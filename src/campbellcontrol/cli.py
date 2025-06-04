import click

import campbellcontrol.commands.commands as commands
from campbellcontrol.config import load_config
from campbellcontrol.connection.aws import AWSConnection
from campbellcontrol.control import AWSCommandHandler


class CommandContext:
    """Create one context object that holds a CommandHandler
    and the rest of the config as attributes - click may have a better way!"""

    def __init__(self, config: dict):
        # TODO - factory for loading the right broker, assume AWS now
        # https://github.com/NERC-CEH/campbell-mqtt-control/issues/14
        # TODO improved error handling
        self.client = AWSConnection("cliclient", config["server"], config["port"])
        self.command_handler = AWSCommandHandler(self.client)

        for key, value in config.items():
            setattr(self, key, value)


@click.group(context_settings={"auto_envvar_prefix": "MQTT"})  # this allows for environment variables
@click.option("--config", default="config.yaml", type=click.Path())
@click.option("--client_id", type=int)
@click.pass_context
def cli(ctx: click.Context, config: str, client_id: int) -> None:
    options = load_config(config)
    if client_id:
        options["client_id"] = client_id
    ctx.obj = CommandContext(options)


@cli.command()
@click.pass_obj
def ls(ctx: CommandContext) -> None:
    """Read and print the list of files on the logger"""
    command = commands.ListFiles(ctx.topic, ctx.client_id, options={"response_suffix": "list"})

    try:
        response = ctx.command_handler.send_command(command)
    except ConnectionError as err:
        click.echo(f"Sorry, couldn't connect to {ctx.server}")
        click.echo(err)
        return

    if response is None:
        click.echo(f"Sorry, couldn't reach {ctx.client_id} on {ctx.server}")
        return

    if response["success"]:
        click.echo(f"Files on device {ctx.client_id}")
        for f in response["payload"]["fileList"]:
            click.echo(f)


@cli.command()
@click.option("--url")
@click.option("--filename")
@click.pass_obj
def put(ctx: CommandContext, url: str, filename: str) -> None:
    """Upload a file at URL onto the location filename"""
    command = commands.Program(ctx.topic, ctx.client_id)

    if not filename and url:
        click.echo("Please suggest a URL to download the script from and a filename for it")
        return

    # TODO question about pre-signed URLs / token authentication
    try:
        response = ctx.command_handler.send_command(command, url, filename)
    except ConnectionError as err:
        click.echo(f"Sorry, couldn't connect to {ctx.server}")
        click.echo(err)
        return

    if response["success"] is False:
        click.echo(f"Couldn't upload {url} as {filename}")

    click.echo(response)


@cli.command()
@click.option("--filename")
@click.pass_obj
def rm(ctx: CommandContext, filename: str) -> None:
    """Delete a named file off the datalogger"""
    command = commands.DeleteFile(ctx.topic, ctx.client_id)
    if not filename:
        click.echo("Please suggest the name of a file you want deleting")
        return

    try:
        response = ctx.command_handler.send_command(command, filename)
    except ConnectionError as err:
        click.echo(f"Sorry, couldn't connect to {ctx.server}")
        click.echo(err)
        return

    if response["success"] is False:
        click.echo(f"Couldn't delete {filename}")

    click.echo(response)


@cli.command()
@click.argument("setting")
@click.pass_obj
def get(ctx: CommandContext, setting: str) -> None:
    """Get the value of a named setting
    TODO add either a command or a help message that returns all names
    """
    command = commands.PublishSetting(ctx.topic, ctx.client_id)
    try:
        response = ctx.command_handler.send_command(command, setting)
    except ConnectionError as err:
        click.echo(f"Sorry, couldn't connect to {ctx.server}")
        click.echo(err)
        return

    print(response)

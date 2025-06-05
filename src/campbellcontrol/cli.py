import logging
from typing import Union

import click

import campbellcontrol.commands.commands as commands
from campbellcontrol.config import load_config
from campbellcontrol.connection.aws import AWSConnection
from campbellcontrol.control import AWSCommandHandler

logging.basicConfig(level=logging.WARNING)


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
    command = commands.ListFiles(ctx.topic, ctx.client_id)

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
    """Upload a file at {URL} to a file named {filename} on the logger"""
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
    """Get the value of a setting on the logger.

    To see a list of all settings, type "mqtt-control settings"
    """
    return get_setting(ctx, setting)


def get_setting(ctx: CommandContext, setting: str) -> None:
    """Show an existing setting on the logger"""
    command = commands.PublishSetting(ctx.topic, ctx.client_id)
    try:
        response = ctx.command_handler.send_command(command, setting)
    except ConnectionError as err:
        click.echo(f"Sorry, couldn't connect to {ctx.server}")
        click.echo(err)
        return
    setting = response["payload"].get("value", None)
    if setting:
        # It comes back padded. We may wish to infer a type or use a mapping
        setting = setting.strip()
    return setting


@cli.command()
def settings() -> str:
    """
    Shows all the settings which you can reset with this tool.

    For reference see the official documentation at
    https://help.campbellsci.com/CR1000X/Content/shared/Maintain/Advanced/settings-general.htm

    """
    with open("settings.txt", "r") as out:
        settings_list = out.read()

    click.echo(settings_list)
    click.echo("https://help.campbellsci.com/CR1000X/Content/shared/Maintain/Advanced/settings-general.htm")


@cli.command()
@click.argument("setting")
@click.argument("value")
@click.pass_obj
def set(ctx: CommandContext, setting: str, value: Union[int, str, float]) -> None:  # noqa: A001
    """Update a setting on the logger"""
    command = commands.SetSetting(ctx.topic, ctx.client_id)
    try:
        response = ctx.command_handler.send_command(command, setting, value)
    except ConnectionError as err:
        click.echo(f"Sorry, couldn't connect to {ctx.server}")
        click.echo(err)
        return

    # Note - you can set values in a range the logger doesn't accept
    # (For example, setting the PakBusAddress to "hello")
    # And it will still return a success response
    # So we should issue a Get to check the value. It comes left padded with spaces

    message = f"Sorry, couldn't set the {setting} to {value}"
    if response["success"]:
        new_value = get_setting(ctx, setting)
        try:
            assert str(new_value) == str(value)
            message = f"Happily set the {setting} to {value}!"
        except AssertionError as err:
            logging.warning(err)

    click.echo(message)

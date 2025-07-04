import dataclasses
import logging
from typing import Any, Union

import click

import campbellcontrol.commands.commands as commands
from campbellcontrol.config import Config, load_config
from campbellcontrol.connection.factory import get_command_handler, get_connection

logger = logging.getLogger("campbellcontrol")
logger.setLevel(logging.INFO)


class CommandContext:
    """Create one context object that holds a CommandHandler
    and the rest of the config as attributes - click may have a better way!"""

    def __init__(self, config: Config, device: str=None):
        self.client = get_connection(config)
        self.command_handler = get_command_handler(self.client)

        for key, value in dataclasses.asdict(config).items():
            setattr(self, key, value)
        if device:
            self.device = device
        elif self.client_id:
            self.device = self.client_id
        logger.info(self.device)
class ControlGroup(click.Group):
    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter) -> Any:
        banner = r"""
_  _  __  ___ ___    ____ ____ __ _ ___ ____ ____ _
|\/| [_,]  |   |  -- |___ [__] | \|  |  |--< [__] |___"""
        formatter.write_heading(banner)
        return super().format_help(ctx, formatter)


@click.group(cls=ControlGroup, context_settings={"auto_envvar_prefix": "MQTT"})  # this allows for environment variables
@click.option("--config", default="config.yaml", type=click.Path())
@click.option("--client_id", type=str)
@click.option("--device_id", type=str)
@click.pass_context
def cli(ctx: click.Context, config: str, client_id: str, device_id: str) -> None:
    options = load_config(config)
    if client_id:
        options.client_id = client_id

    ctx.obj = CommandContext(options, device=device_id)


@cli.command()
@click.pass_obj
def ls(ctx: CommandContext) -> None:
    """Read and print the list of files on the logger"""
    command = commands.ListFiles(ctx.topic, ctx.device)

    try:
        response = ctx.command_handler.send_command(command)
    except ConnectionError as err:
        click.echo(f"Sorry, couldn't connect to {ctx.server}")
        click.echo(err)
        return

    if response is None:
        click.echo(f"Sorry, couldn't reach {ctx.device} on {ctx.server}")
        return

    if "success" in response and response["success"]:
        click.secho(f"\nFiles on device {ctx.device}:\n", fg="green")
        for f in response["payload"]["fileList"]:
            click.echo(f)


@cli.command()
@click.option("--url")
@click.option("--filename")
@click.pass_obj
def put(ctx: CommandContext, url: str, filename: str) -> None:
    """Upload a file at {URL} to a file named {filename} on the logger"""
    command = commands.Program(ctx.topic, ctx.device)

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

    if "error" in response:
        click.secho(f"Couldn't upload {url} as {filename}", fg="yellow")
        return

    message = response["payload"]["success"]
    click.secho(f"{message}!", fg="green")


@cli.command()
@click.option("--filename")
@click.pass_obj
def rm(ctx: CommandContext, filename: str) -> None:
    """Delete a named file off the datalogger"""
    command = commands.DeleteFile(ctx.topic, ctx.device)
    if not filename:
        click.echo("Please suggest the name of a file you want deleting")
        return

    try:
        response = ctx.command_handler.send_command(command, filename)
    except ConnectionError as err:
        click.echo(f"Sorry, couldn't connect to {ctx.server}")
        click.echo(err)
        return

    if "error" in response:
        click.secho(f"Couldn't delete {filename}", fg="yellow")
    elif "success" in response:
        message = response["payload"]["success"]
        click.secho(f"{message}!", fg="green")


@click.argument("setting")
@click.pass_obj
def get(ctx: CommandContext, setting: str) -> None:
    """Get the value of a setting on the logger.

    To see a list of all settings, type "mqtt-control settings"
    """
    return get_setting(ctx, setting)


def get_setting(ctx: CommandContext, setting: str) -> None:
    """Show an existing setting on the logger"""
    command = commands.PublishSetting(ctx.topic, ctx.device)
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
    command = commands.SetSetting(ctx.topic, ctx.device)
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


@cli.command()
@click.argument("setting")
@click.argument("value")
@click.pass_obj
def setvar(ctx: CommandContext, setting: str, value: Union[int, str, float]) -> None:  # noqa: A001
    """Update a script variable on the logger.
    Hopefully useful for adaptive sampling!"""
    command = commands.SetVar(ctx.topic, ctx.device)
    try:
        response = ctx.command_handler.send_command(command, setting, value)
    except ConnectionError as err:
        click.echo(f"Sorry, couldn't connect to {ctx.server}")
        click.echo(err)
        return

    if response["success"]:
        click.echo(response)
    else:
        click.echo(response)
    # TODO be informative about likely reasons for error


@cli.command()
@click.argument("setting")
@click.pass_obj
def getvar(ctx: CommandContext, setting: str) -> None:  # noqa: A001
    """Get the value of a script variable on the logger.
    (E.g. anything defined as "Public" in the running script.)
    """
    command = commands.GetVar(ctx.topic, ctx.device)
    try:
        response = ctx.command_handler.send_command(command, setting)
    except ConnectionError as err:
        click.echo(f"Sorry, couldn't connect to {ctx.server}")
        click.echo(err)
        return

    if response["success"]:
        name = response["payload"]["name"]
        value = response["payload"]["value"]
        click.echo(f"Happily set {name} to {value}")
    else:
        if "varname" in response:
            click.echo(f"No variable named {response['varname']} to set")
        else:
            click.echo(response)


@cli.command()
@click.pass_obj
def reboot(ctx: CommandContext) -> None:
    """Reboot the logger! Use with caution"""
    click.confirm(f"Are you sure you want to reboot logger {ctx.device}?", abort=True)
    command = commands.Reboot(ctx.topic, ctx.device)
    try:
        response = ctx.command_handler.send_command(command)
    except ConnectionError as err:
        click.echo(f"Sorry, couldn't connect to {ctx.server}")
        click.echo(err)
        return

    if response is None:
        click.secho(f"Sorry, couldn't reach {ctx.device} on {ctx.server}", fg="yellow")
        return
    if "success" in response and response["success"]:
        click.secho(
            f"Successfully ran: {response['payload']['reason']} for {response['payload']['clientId']}", fg="green"
        )

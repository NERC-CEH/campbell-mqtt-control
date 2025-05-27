import click

import campbellcontrol.commands.commands as commands
from campbellcontrol.config import load_config


@click.group(context_settings={"auto_envvar_prefix": "FOOP"})  # this allows for environment variables
@click.option("--config", default="config.yaml", type=click.Path())  # this allows us to change config path
@click.pass_context
def cli(ctx: click.Context, config: str) -> None:
    # TODO here we need to add context from the config both for the individual Commands,
    # _and_ context for the command handler (whose class we infer from the broker type passed in the config)
    ctx.obj = load_config(config)


@cli.command()
@click.pass_obj
def ls(config: dict) -> None:
    commands.ListFiles(config["topic"], config["serial"], options={"response_suffix": "list"})
    # TODO wire up the command handler properly
    click.echo(f"ls {config['serial']}")

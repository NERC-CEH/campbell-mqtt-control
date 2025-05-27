import click

from campbellcontrol.config import load_config


# @click.group(context_settings={'auto_envvar_prefix': 'FOOP'})  # this allows for environment variables
@click.option("--config", default="config.yml", type=click.Path())  # this allows us to change config path
@click.pass_context
def mqtt(ctx: click.Context, config: str) -> None:
    ctx.default_map = load_config(config)


@mqtt.command()
def ls() -> None:
    click.echo()


@mqtt.command()
def cli() -> None:
    """Prints a greeting."""
    click.echo("Hello, World!")

import click


@click.command()
def cli() -> None:
    """Prints a greeting."""
    click.echo("Hello, World!")

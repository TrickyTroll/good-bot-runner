import click
import funcmodule


@click.group()
def app():
    """Automating the recording of documentation videos."""
    pass


@click.command()
def greet():
    """Greets the user.

    Returns:
        None: None
    """
    click.echo("Hello, world!")

    return None


@click.command()
@click.argument(
    "config",
    type=click.File("r")
)
def echo_config(config: click.File) -> None:
    """To echo the configuration file

    Args:
        config (click.File): The config file provided by the user.
    Returns:
        None: None
    """
    parsed = funcmodule.config_parser(config)
    click.echo(parsed)
    return None


@click.command()
@click.argument(
    "config",
    type=click.File("r")
)
@click.option(
    "--project-name",
    prompt='''\
    Please provide a name for your project.
    ''')
def setup(config: click.File, project_name: str) -> None:
    """Create a directory that contains everything required to make
    a documentation video!

    Args:
        config (click.File): The configuration file. This should be
        handled by click.
        project_name (str): The name of the project. Will be used
        to create the project's root directory.

    Returns:
        None: None
    """
    to_create = []

    todos = funcmodule.create_classes(config)
    for todo in todos:
        if todo.get_directory() not in to_create:
            to_create.append(todo.get_directory())

    path = funcmodule.create_dirs(to_create, project_name)

    click.echo(f"Your project has been setup at: {path}.")

    return None


app.add_command(setup)
app.add_command(greet)
app.add_command(echo_config)

if __name__ == "__main__":
    app()
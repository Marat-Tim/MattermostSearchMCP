from mm import get_team_id
from mm_search_mcp import mcp
import typer
from config import *
from tool import *
from tool.search import search_impl
from tool.thread import thread_impl

cli = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    help=f"""Mattermost MCP server
    
    The server URL must be specified in the {mm_url.name} variable, for example, `https://mattermost.raiffeisen.ru`.
    To work, the utility must call the Mattermost API. There are two authorization methods for this:
    1. Obtain an official Mattermost token and set it to the {mm_token.name} variable
    2. Retrieve the {mm_auth_token.name}, {mm_user_id.name}, and {mm_csrf.name} cookies from the browser and set them to the variables of the same name
    If you have problem with ssl certificates you can set {mm_verify_ssl.name} to 
    - True(use default certificate)
    - False(do not use ssl)
    - Raif_Default(certificate for raiffeisen mattermost instance)
    - Filepath with certificate
    
    {variables_status()}
    """
)


@cli.command()
def check():
    """
    Check, that environment configured correctly and mattermost api call working
    """
    typer.echo(variables_status(md=False))
    if not is_browser_active() and not is_official_active():
        typer.echo("No auth provided")
        raise typer.Exit(1)
    typer.echo("Checking Mattermost API:")
    typer.echo("get_team_id(): ", nl=False)
    try:
        team_id = get_team_id()
        typer.echo(f"working good, team_id={team_id}")
    except Exception as e:
        typer.echo(f"call failed, {e}")
        raise typer.Exit(1)
    typer.echo('search("test", 0): ', nl=False)
    try:
        search_res = search_impl("test", 0)
        typer.echo(f"working good, found {len(search_res)} matches")
    except Exception as e:
        typer.echo(f"call failed, {e}")
        raise typer.Exit(1)
    if len(search_res) != 0:
        typer.echo(f'thread("{search_res[0]["thread_id"]}"): ', nl=False)
        try:
            posts = thread_impl(search_res[0]["thread_id"])
            typer.echo(f"working good, get {len(posts)} posts")
        except Exception as e:
            typer.echo(f"call failed, {e}")
            raise typer.Exit(1)


@cli.command()
def run():
    """
    Run local MCP server with stdio transport
    """
    if not is_browser_active() and not is_official_active():
        typer.echo(variables_status(md=False))
        typer.echo("No auth provided")
        raise typer.Exit(1)
    mcp.run()


if __name__ == "__main__":
    cli()

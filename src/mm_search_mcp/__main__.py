import browsercookie

from mm_search_mcp.mm import get_team_id, get_team_name
from mm_search_mcp.server import mcp
import typer
from mm_search_mcp.config import *
from mm_search_mcp.tool import *
from mm_search_mcp.tool.search import search_impl
from mm_search_mcp.tool.thread import thread_impl

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
    """,
)

@cli.command()
def extract_auth_from_browser():
    """
    Extract MMAUTHTOKEN, MMUSERID, MMCSRF from the browser cookies and print them
    """
    for cookie in browsercookie.load():
        if cookie.name in {"MMAUTHTOKEN", "MMUSERID", "MMCSRF"}:
            typer.echo(f'export {cookie.name}="{cookie.value}"')
    typer.echo("Add this variables to your config(~/.zshrc or ~/.bash_profile)")


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
    typer.echo("get_team(): ", nl=False)
    try:
        team_id = get_team_id()
        team_name = get_team_name()
        typer.echo(f"working good, id={team_id}, name={team_name}")
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


def main():
    cli()


if __name__ == "__main__":
    main()

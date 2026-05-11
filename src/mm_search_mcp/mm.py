from functools import cache

from mattermost_api_reference_client import AuthenticatedClient
from mattermost_api_reference_client.api.teams import get_all_teams
from mattermost_api_reference_client.models import Team

from .config import *

client = None
if is_browser_active():
    client = AuthenticatedClient(
        base_url=mm_url.value(),
        token=mm_auth_token.value(),
        cookies={
            "MMAUTHTOKEN": mm_auth_token.value(),
            "MMUSERID": mm_user_id.value(),
            "MMCSRF": mm_csrf.value(),
        },
        headers={
            "x-csrf-token": mm_csrf.value(),
        },
    )
if is_official_active():
    client = AuthenticatedClient(base_url=mm_url.value(), token=mm_token.value())
if client is not None:
    val = mm_verify_ssl.value()
    if val == "Raif_Default":
        from .raif_ssl import context

        client._verify_ssl = context
    elif val.upper() == "TRUE":
        client._verify_ssl = True
    elif val.upper() == "FALSE":
        client._verify_ssl = False
    else:
        client._verify_ssl = val


@cache
def get_team() -> Team:
    teams = get_all_teams.sync(client=client)
    return teams[0]


def get_team_id() -> str:
    return get_team().id


def get_team_name() -> str:
    return get_team().name


def link_to(post_id: str) -> str:
    return f"{mm_url.value()}/{get_team_name()}/pl/{post_id}"

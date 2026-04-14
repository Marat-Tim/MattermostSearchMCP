import os

import requests
from anyio.functools import cache

from config import log_to_file_enabled, logs_file


def log_to_file(text) -> None:
    if log_to_file_enabled:
        with open(logs_file, "a") as f:
            f.write(str(text) + "\n")


def get_mm_url() -> str:
    return "https://mattermost.raiffeisen.ru/api/v4"


def get_team_id() -> str:
    return "tokxfg1eff8pjpkmg69wrhrbey"


session = requests.session()
session.cookies.update(
    {
        "MMAUTHTOKEN": str(os.getenv("MMAUTHTOKEN")),
        "MMUSERID": str(os.getenv("MMUSERID")),
        "MMCSRF": str(os.getenv("MMCSRF")),
    }
)
session.headers.update(
    {
        "x-csrf-token": str(os.getenv("MMCSRF")),
    }
)

def get_channels() -> list:
    rs = session.get(f"{get_mm_url()}/users/me/channels").json()
    result = list()
    for channel in rs:
        result.append(
            {
                "id": channel["id"],
                "display_name": channel["display_name"],
                "name": channel["name"],
            }
        )
    return result

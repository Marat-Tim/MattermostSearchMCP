import json
import os

import requests
from fastmcp import FastMCP
import pydantic

mcp = FastMCP("Mattermost search MCP")

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

def get_mm_url() -> str:
    return "https://mattermost.raiffeisen.ru/api/v4"

def get_team_id() -> str:
    return "tokxfg1eff8pjpkmg69wrhrbey"

class SearchRq(pydantic.BaseModel):
    terms: str = pydantic.Field(description="The search terms as inputed by the user. To search for posts from a user include from:someusername, using a user's username. To search in a specific channel include in:somechannel, using the channel name (not the display name).")
    page: int = pydantic.Field(description="The page number to search in. Starts with 0.")

@mcp.tool(description="Search in messages")
def search(search: SearchRq) -> str:
    rs = session.post(
        f"{get_mm_url()}/teams/{get_team_id()}/posts/search",
        json={
            "include_deleted_channels": True,
            "is_or_search": False,
            "page": search.page,
            "per_page": 30,
            "terms": search.terms,
            "time_zone_offset": 10800
        },
    ).json()
    result = list()
    for order_id in rs["order"]:
        el = rs["posts"][order_id]
        result.append(
            {
                "id": el["id"],
                "user_id": el["user_id"],
                "channel_id": el["channel_id"],
                "message": el["message"],
                "reply_count": el["reply_count"],
            }
        )
    return json.dumps(result)


if __name__ == "__main__":
    mcp.run()

from mattermost_api_reference_client.api.users import get_users_by_ids

from mm_search_mcp import mcp
from mm import client


@mcp.tool
def users_by_ids(user_ids: list[str]):
    rs = get_users_by_ids.sync(
        body=user_ids,
        client=client,
    )
    return [
        {
            "id": el.id,
            "username": el.username,
            "first_name": el.first_name,
            "last_name": el.last_name,
            "email": el.email,
            "nickname": el.nickname,
        }
        for el in rs
    ]

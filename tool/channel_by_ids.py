from mattermost_api_reference_client.api.channels import get_channels_for_user

from mm_search_mcp import mcp
from mm import client


@mcp.tool
def channel_by_ids(ids: list[str]):
    rs = get_channels_for_user.sync(
        "me",
        client=client,
    )
    return [
        {
            "id": el.id,
            "name": el.name,
            "display_name": el.display_name,
        }
        for el in rs if rs.id in ids
    ]

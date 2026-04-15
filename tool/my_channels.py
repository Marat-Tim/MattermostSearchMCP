from mattermost_api_reference_client.api.channels import get_channels_for_user

from mm import client
from mm_search_mcp import mcp


@mcp.tool
def my_channels():
    rs = get_channels_for_user.sync(
        "me",
        client=client,
    )
    return [
        {
            "name": el.name,
            "display_name": el.display_name,
        }
        for el in rs
    ]


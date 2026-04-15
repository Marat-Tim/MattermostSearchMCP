from mattermost_api_reference_client.api.channels import get_channels_for_user

from mm_search_mcp import mcp
from mm import client


@mcp.tool(description="Get channels by display name(!!! IMPORTANT: not by id)")
def channel_by_display_name(display_name: str):
    rs = get_channels_for_user.sync(
        "me",
        client=client,
    )
    for el in rs:
        if el.display_name == display_name:
            return {
                "id": el.id,
                "name": el.name,
                "display_name": el.display_name,
            }
    return "Not found"

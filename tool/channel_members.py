from mattermost_api_reference_client.api.channels import get_channel_members

from mm_search_mcp import mcp
from mm import client


@mcp.tool
def channel_members(channel_id: str):
    rs = get_channel_members.sync(
        channel_id,
        client=client,
    )
    return [member.user_id for member in rs]

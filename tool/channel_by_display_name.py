from fastmcp import FastMCP

from util import get_channels

tool_name = "Get channel name by display name"


def register_in(mcp: FastMCP):
    @mcp.tool(description=tool_name)
    def channel_by_display_name(display_name: str):
        channels = get_channels()
        for channel in channels:
            if channel["display_name"] == display_name:
                return channel
        return None

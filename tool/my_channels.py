import json

from fastmcp import FastMCP

from util import get_channels

tool_name = "Get all my channels"

def register_in(mcp: FastMCP):
    @mcp.tool(description=tool_name)
    def channels() -> str:
        return json.dumps(get_channels(), ensure_ascii=False)
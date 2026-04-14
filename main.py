from fastmcp import FastMCP

from tool import my_channels, search, channel_by_display_name
from util import log_to_file

mcp = FastMCP(
    "Mattermost search MCP",
    instructions=f"""
    Since the user works with channel names via 'displayName', 
    it makes sense to call '{channel_by_display_name.tool_name}' whenever a name is mentioned 
    """
)

my_channels.register_in(mcp)
search.register_in(mcp)
channel_by_display_name.register_in(mcp)

if __name__ == "__main__":
    try:
        mcp.run()
    except Exception as e:
        log_to_file(str(e))

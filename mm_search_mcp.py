from fastmcp import FastMCP

mcp = FastMCP(
    "Mattermost search MCP",
    instructions=f"""
    It's normal to make a lot of calls to retrieve related objects.
    !!! VERY IMPORTANT: Never give users the "id" field(or channel_id, user_id e.g)
    because they won't understand what it means.
    You need to use other tools to find proper names based on those IDs.
    """
)

from fastmcp import FastMCP

mcp = FastMCP(
    "Mattermost search MCP",
    instructions=f"""
    Company mattermost address is `https://mattermost.raiffeisen.ru/raiffeisenbank`.
    Links to message typically looks like `https://mattermost.raiffeisen.ru/raiffeisenbank/pl/j6pwd78ge7rmuf5gfuknb8wbec`.
    Last part of path is ID of message.
    If user want to get message, do not send id of message. You must create link and send link. 
    !!! VERY IMPORTANT: Never give users the "id" field(or channel_id, user_id e.g)
    because they won't understand what it means.
    """
)

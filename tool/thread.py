from mattermost_api_reference_client.api.posts import get_post_thread

from mm_search_mcp import mcp
from mm import client


@mcp.tool
def thread(post_id: str):
    rs = get_post_thread.sync(
        post_id,
        client=client
    )
    return [
        {
            "message": post.message,
            "user_id": post.user_id,
        }
        for post in sorted(rs.posts.additional_properties.values(), key=lambda p: (p.create_at, p.id))
    ]

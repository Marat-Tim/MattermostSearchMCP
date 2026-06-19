from datetime import datetime

from mattermost_api_reference_client.api.posts import get_post_thread
from mattermost_api_reference_client.api.users import get_users_by_ids

from mm_search_mcp.server import mcp
from mm_search_mcp.mm import client, link_to


def thread_impl(thread_id: str):
    rs = get_post_thread.sync(thread_id, client=client)
    users = get_users_by_ids.sync(
        body=[post.user_id for post in rs.posts.additional_properties.values()],
        client=client,
    )
    users_map = {
        user.id: {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "nickname": user.nickname,
        }
        for user in users
    }
    return [
        {
            "link": link_to(post.id),
            "message": post.message,
            "user": users_map[post.user_id],
            "date": datetime.fromtimestamp(post.create_at / 1000.0),
        }
        for post in sorted(
            rs.posts.additional_properties.values(), key=lambda p: (p.create_at, p.id)
        )
    ]


@mcp.tool
def thread(thread_id: str):
    return thread_impl(thread_id)

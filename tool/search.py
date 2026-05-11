from mattermost_api_reference_client.api.posts import search_posts
from mattermost_api_reference_client.api.users import get_users_by_ids
from mattermost_api_reference_client.api.channels import get_channels_for_user, get_channel_members
from mattermost_api_reference_client.models import SearchPostsBody

from mm_search_mcp import mcp
from mm import client, get_team_id


def search_impl(terms: str, page: int):
    rs = search_posts.sync(
        get_team_id(),
        body=SearchPostsBody(
            terms=terms,
            is_or_search=False,
            page=page,
            per_page=30,
            time_zone_offset=10800
        ),
        client=client
    )
    users = get_users_by_ids.sync(
        body=[el.user_id for el in rs.posts.additional_properties.values()],
        client=client
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
    channels = get_channels_for_user.sync("me", client=client)
    channels_map = {
        channel.id:
            {
                "name": channel.name,
                "display_name": ", ".join([
                    user.first_name + " " + user.last_name
                    for user in get_users_by_ids.sync(
                        body=[
                            str(member.user_id)
                            for member in get_channel_members.sync(
                                channel.id,
                                client=client
                            )
                        ],
                        client=client
                    )
                ]),
            }
            if channel.type_ == "D" else
            {
                "name": channel.name,
                "display_name": channel.display_name,
            }
        for channel in channels
        if channel.id in [post.channel_id for post in rs.posts.additional_properties.values()]
    }
    return [
        {
            "thread_id": el.id,
            "user": users_map[el.user_id],
            "channel": channels_map[el.channel_id],
            "message": el.message,
            "reply_count": el.to_dict()["reply_count"],
        } for el in rs.posts.additional_properties.values()
    ]

@mcp.tool
def search(terms: str, page: int):
    """
    :param terms: The search terms as inputed by the user.
        To search for posts from a user include from:someusername, using a user's username.
        To search in a specific channel include in:somechannel,
        using the channel name
        (not the display name, you can get channel name using tool 'Get channel name by display name').
    :param page: The page number to search in. Starts with 0.
    """
    return search_impl(terms, page)

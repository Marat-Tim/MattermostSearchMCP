from mattermost_api_reference_client.api.posts import search_posts
from mattermost_api_reference_client.models import SearchPostsBody

from mm_search_mcp import mcp
from mm import client, get_team_id


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
    return [
        {
            "id": el.id,
            "user_id": el.user_id,
            "channel_id": el.channel_id,
            "message": el.message,
            "reply_count": el.to_dict()["reply_count"],
        } for el in rs.posts.additional_properties.values()
    ]

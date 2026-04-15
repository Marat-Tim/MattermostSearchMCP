import json

from fastmcp import FastMCP
from ratelimit import limits, RateLimitException

from util import log_to_file, get_mm_url, get_team_id, session


def register_in(mcp: FastMCP):
    @limits(calls=1, period=2)
    def _search(terms: str, page: int) -> str:
        rs = session.post(
            f"{get_mm_url()}/teams/{get_team_id()}/posts/search",
            json={
                "include_deleted_channels": True,
                "is_or_search": False,
                "page": page,
                "per_page": 30,
                "terms": terms,
                "time_zone_offset": 10800
            },
        ).json()
        log_to_file(rs)
        result = list()
        for order_id in rs["order"]:
            el = rs["posts"][order_id]
            result.append(
                {
                    "id": el["id"],
                    "user_id": el["user_id"],
                    "channel_id": el["channel_id"],
                    "message": el["message"],
                    "reply_count": el["reply_count"],
                }
            )
        result_json = json.dumps(result, ensure_ascii=False)
        log_to_file(result_json)
        return result_json

    @mcp.tool(description="Search in messages")
    def search(terms: str, page: int) -> str:
        """
        :param terms: The search terms as inputed by the user.
            To search for posts from a user include from:someusername, using a user's username.
            To search in a specific channel include in:somechannel,
            using the channel name
            (not the display name, you can get channel name using tool 'Get channel name by display name').
        :param page: The page number to search in. Starts with 0.
        """
        try:
            return _search(terms, page)
        except RateLimitException as e:
            return json.dumps(
                {
                    "status": "error",
                    "error": "Rate limit exceeded",
                    "retry_after_seconds": e.period_remaining
                }
            )

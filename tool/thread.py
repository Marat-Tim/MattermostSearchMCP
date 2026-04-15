import json

from fastmcp import FastMCP

from util import session, get_mm_url, log_to_file

tool_name = "Get thread"


def register_in(mcp: FastMCP):
    @mcp.tool(description=tool_name)
    def thread(post_id: str) -> str:
        """
        :param post_id: id of any message from thread
        """
        rs = session.get(f"{get_mm_url()}/posts/{post_id}/thread").json()
        log_to_file(rs)
        result = json.dumps(
            [
                {key: el[key] for key in ["message", "user_id"]}
                for el in sorted(rs["posts"].values(), key=lambda p: (p["create_at"], p["id"]))
            ],
            ensure_ascii=False
        )
        log_to_file(result)
        return result

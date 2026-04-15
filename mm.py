import os

from mattermost_api_reference_client import AuthenticatedClient

client = AuthenticatedClient(
    base_url="https://mattermost.raiffeisen.ru",
    token=str(os.getenv("MMAUTHTOKEN")),
    cookies={
        "MMAUTHTOKEN": str(os.getenv("MMAUTHTOKEN")),
        "MMUSERID": str(os.getenv("MMUSERID")),
        "MMCSRF": str(os.getenv("MMCSRF")),
    },
    headers={
        "x-csrf-token": str(os.getenv("MMCSRF")),
    },
    verify_ssl="/Users/ruabgmj/Developer/raif/ruabgmj/mm-search-mcp/certs/mattermost.raiffeisen.ru.pem"
)

def get_team_id() -> str:
    return "tokxfg1eff8pjpkmg69wrhrbey"

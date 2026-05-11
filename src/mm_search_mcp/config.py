import os


class EnvVar:
    def __init__(self, name: str, private: bool = False, default: str | None = None):
        self.name = name
        self.private = private
        self.default = default

    def value(self) -> str:
        var = os.getenv(self.name)
        if var is None:
            if self.default is not None:
                return self.default
            raise Exception(f"Env var {self.name} not defined")
        return var

    def exists(self) -> bool:
        if self.default is not None:
            return True
        var = os.getenv(self.name)
        return var is not None

    def __str__(self) -> str:
        if self.exists():
            return f"{self.name}=`{"***" if self.private else self.value()}`{" (default value)" if self.default else ""}"
        else:
            return f"{self.name} is not defined"


mm_url = EnvVar("MM_URL", default="https://mattermost.raiffeisen.ru")
mm_token = EnvVar("MM_TOKEN", private=True)
mm_auth_token = EnvVar("MMAUTHTOKEN", private=True)
mm_user_id = EnvVar("MMUSERID", private=True)
mm_csrf = EnvVar("MMCSRF", private=True)
mm_verify_ssl = EnvVar("MM_VERIFY_SSL", default="Raif_Default")


def is_official_active() -> bool:
    return mm_url.exists() and mm_token.exists()


def is_browser_active() -> bool:
    return mm_url.exists() and mm_auth_token.exists() and mm_user_id.exists() and mm_csrf.exists()


def variables_status(md: bool = True) -> str:
    md_text = "    " if md else ""
    return f"""{mm_url}
    
{md_text}1. Official API Token {"[Configured, Active]" if is_official_active() else ""}
{md_text}  - {mm_token}
{md_text}2. Browser cookies {("[Configured]" if is_official_active() else "[Configured, Active]") if is_browser_active() else ""} 
{md_text}  - {mm_auth_token}
{md_text}  - {mm_user_id}
{md_text}  - {mm_csrf}

{md_text}{mm_verify_ssl}
    """

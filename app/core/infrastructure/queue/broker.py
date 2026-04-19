import os
from urllib.parse import quote

from dotenv import load_dotenv
from taskiq_redis import RedisStreamBroker

load_dotenv()


def build_redis_url() -> str:
    username = os.getenv("REDIS__USERNAME", "")
    password = os.getenv("REDIS__PASSWORD", "")
    host = os.getenv("REDIS__HOST", "localhost")
    port = os.getenv("REDIS__PORT", "6379")
    db = os.getenv("REDIS__DB", "0")

    username_enc = quote(username, safe="")
    password_enc = quote(password, safe="")

    auth_part = ""
    if username_enc or password_enc:
        auth_part = f"{username_enc}:{password_enc}@"

    return f"redis://{auth_part}{host}:{port}/{db}"


broker = RedisStreamBroker(url=build_redis_url())

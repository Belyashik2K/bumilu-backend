from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

security = HTTPBearer(auto_error=False)


def get_bearer_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    if not credentials:
        raise ValueError("Authorization header missing or invalid")
    return credentials.credentials

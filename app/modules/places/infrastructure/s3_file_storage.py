from typing import Final

from aiobotocore.session import get_session
from botocore.config import Config
from botocore.exceptions import ClientError

from app.modules.places.application.interfaces.file_storage import (
    FileObjectInfo,
    IFileStorage,
)


class S3FileStorage(IFileStorage):
    _SERVICE_NAME: Final[str] = "s3"

    def __init__(
        self,
        *,
        bucket_name: str,
        region_name: str,
        endpoint_url: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_session_token: str | None = None,
        verify_ssl: bool | str = True,
    ) -> None:
        self._bucket_name = bucket_name
        self._region_name = region_name
        self._endpoint_url = endpoint_url
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self._aws_session_token = aws_session_token
        self._verify_ssl = verify_ssl
        self._session = get_session()

        self._config = Config(
            signature_version="s3v4",
            s3={"addressing_style": "path"},
        )

    def _client_kwargs(self) -> dict:
        return {
            "service_name": self._SERVICE_NAME,
            "region_name": self._region_name,
            "endpoint_url": self._endpoint_url,
            "aws_access_key_id": self._aws_access_key_id,
            "aws_secret_access_key": self._aws_secret_access_key,
            "aws_session_token": self._aws_session_token,
            "verify": self._verify_ssl,
            "config": self._config,
        }

    async def generate_upload_url(
        self,
        file_key: str,
        content_type: str,
        expires_in: int = 3600,
    ) -> str:
        async with self._session.create_client(**self._client_kwargs()) as client:
            url = await client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": self._bucket_name,
                    "Key": file_key,
                    "ContentType": content_type,
                },
                ExpiresIn=expires_in,
                HttpMethod="PUT",
            )
            return url

    async def get_object_info(
        self,
        *,
        file_key: str,
    ) -> FileObjectInfo | None:
        async with self._session.create_client(**self._client_kwargs()) as client:
            try:
                response = await client.head_object(
                    Bucket=self._bucket_name,
                    Key=file_key,
                )
            except ClientError as exc:
                error_code = (
                    exc.response.get("Error", {}).get("Code")
                    if exc.response is not None
                    else None
                )

                if error_code in {"404", "NoSuchKey", "NotFound"}:
                    return None

                raise

        etag = response.get("ETag")
        if isinstance(etag, str):
            etag = etag.strip('"')

        return FileObjectInfo(
            file_key=file_key,
            content_type=response.get("ContentType"),
            size=response.get("ContentLength"),
            etag=etag,
        )

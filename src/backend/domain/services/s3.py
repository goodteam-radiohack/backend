from dataclasses import dataclass
from datetime import timedelta

from backend.infrastructure.hack import S3Bucket
from backend.infrastructure.settings import AppSettings


@dataclass
class S3Service:
    settings: AppSettings
    bucket: S3Bucket

    async def upload(
        self, key: str, data: bytes, content_type: str = "application/octet-stream"
    ) -> None:
        await self.bucket.put_object(
            Bucket=self.settings.s3.bucket, Key=key, Body=data, ContentType=content_type
        )

    async def get_url(self, key: str, expires_in: timedelta) -> str:
        params = {"Bucket": self.settings.s3.bucket, "Key": key}

        return str(
            await self.bucket.generate_presigned_url(
                ClientMethod="get_object",
                Params=params,
                ExpiresIn=int(expires_in.total_seconds()),
            )
        )

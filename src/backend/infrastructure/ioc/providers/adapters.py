from collections.abc import AsyncIterator

import aioboto3
from async_firebase import AsyncFirebaseClient
from dishka import Provider, Scope, provide

from backend.domain.services.s3 import S3Service
from backend.infrastructure.hack import S3Bucket
from backend.infrastructure.settings import AppSettings


class S3Provider(Provider):
    scope = Scope.APP

    @provide
    async def provide_s3_bucket(self, settings: AppSettings) -> AsyncIterator[S3Bucket]:
        session = aioboto3.Session()

        async with session.client(
            service_name="s3",
            region_name=settings.s3.region,
            endpoint_url=settings.s3.endpoint,
            aws_access_key_id=settings.s3.access_key.get_secret_value(),
            aws_secret_access_key=settings.s3.secret_key.get_secret_value(),
        ) as s3:
            yield s3

    s3_service = provide(S3Service)


class FirebaseProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_firebase(self, settings: AppSettings) -> AsyncFirebaseClient:
        client = AsyncFirebaseClient()
        client.creds_from_service_account_info(settings.google.data)

        return client

from dishka import Provider, Scope, from_context, provide
from fastapi import Request

from backend.application.common.id_provider import IdProvider
from backend.application.common.token_processor import TokenProcessor
from backend.infrastructure.auth.id_provider import UserIdProvider
from backend.infrastructure.auth.jwt_processor import JWTProcessor


class AuthProvider(Provider):
    scope = Scope.REQUEST

    request = from_context(Request)
    id_provider = provide(UserIdProvider, provides=IdProvider)

    jwt_processor = provide(JWTProcessor, provides=TokenProcessor, scope=Scope.APP)

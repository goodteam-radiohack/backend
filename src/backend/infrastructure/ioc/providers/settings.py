from dishka import Provider, Scope, provide

from backend.infrastructure.settings import AppSettings, get_settings


class SettingsProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_settings(self) -> AppSettings:
        return get_settings()

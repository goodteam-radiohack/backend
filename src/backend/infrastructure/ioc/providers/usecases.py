from dishka import Provider, Scope, provide

from backend.application.common.uow import UnitOfWork
from backend.infrastructure.database.uow import UnitOfWorkImpl


class UsecasesProvider(Provider):
    scope = Scope.REQUEST

    uow = provide(UnitOfWorkImpl, provides=UnitOfWork)

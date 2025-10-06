from dishka import Provider, Scope, provide

from backend.application.common.uow import UnitOfWork
from backend.application.usecases.auth.logout import LogOutUseCase
from backend.application.usecases.auth.signin import SignInUseCase
from backend.application.usecases.users.me import MeUseCase
from backend.application.usecases.events.get import GetEventsUseCase
from backend.infrastructure.database.uow import UnitOfWorkImpl


class UsecasesProvider(Provider):
    scope = Scope.REQUEST

    # auth
    signin = provide(SignInUseCase)
    logout = provide(LogOutUseCase)

    # users
    me = provide(MeUseCase)

    # events
    get_events = provide(GetEventsUseCase)

    # rsvp

    uow = provide(UnitOfWorkImpl, provides=UnitOfWork)

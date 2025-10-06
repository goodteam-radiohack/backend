from dishka import Provider, Scope, provide

from backend.application.common.uow import UnitOfWork
from backend.application.usecases.auth.logout import LogOutUseCase
from backend.application.usecases.auth.signin import SignInUseCase
from backend.application.usecases.catalogs.get import GetCatalogUseCase
from backend.application.usecases.catalogs.get_root import GetRootCatalogsUseCase
from backend.application.usecases.documents.create import CreateDocumentUseCase
from backend.application.usecases.documents.delete import DeleteDocumentUseCase
from backend.application.usecases.documents.get import GetDocumentUseCase
from backend.application.usecases.documents.upload import UploadDocumentUseCase
from backend.application.usecases.events.get import GetEventsUseCase
from backend.application.usecases.rsvp.set_status import SetRsvpStatusUseCase
from backend.application.usecases.users.me import GetMeUseCase
from backend.infrastructure.database.uow import UnitOfWorkImpl
from backend.application.usecases.catalogs.delete import DeleteCatalogUseCase


class UsecasesProvider(Provider):
    scope = Scope.REQUEST

    # auth
    signin = provide(SignInUseCase)
    logout = provide(LogOutUseCase)

    # users
    me = provide(GetMeUseCase)

    # events
    get_events = provide(GetEventsUseCase)

    # rsvp
    set_rsvp_status = provide(SetRsvpStatusUseCase)

    # catalogs
    get_root_catalogs = provide(GetRootCatalogsUseCase)
    get_catalog = provide(GetCatalogUseCase)
    delete_catalog = provide(DeleteCatalogUseCase)

    # documents
    get_document = provide(GetDocumentUseCase)
    upload_document = provide(UploadDocumentUseCase)
    create_document = provide(CreateDocumentUseCase)
    delete_document = provide(DeleteDocumentUseCase)

    uow = provide(UnitOfWorkImpl, provides=UnitOfWork)

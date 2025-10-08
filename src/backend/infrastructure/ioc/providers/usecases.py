from dishka import Provider, Scope, provide

from backend.application.common.uow import UnitOfWork
from backend.application.usecases.auth.logout import LogOutUseCase
from backend.application.usecases.auth.signin import SignInUseCase
from backend.application.usecases.catalogs.create import CreateCatalogUseCase
from backend.application.usecases.catalogs.delete import DeleteCatalogUseCase
from backend.application.usecases.catalogs.get import GetCatalogUseCase
from backend.application.usecases.catalogs.get_root import GetRootCatalogsUseCase
from backend.application.usecases.devices.register import RegisterDeviceUseCase
from backend.application.usecases.devices.send_notifications import (
    SendNotificationsUseCase,
)
from backend.application.usecases.documents.create import CreateDocumentUseCase
from backend.application.usecases.documents.delete import DeleteDocumentUseCase
from backend.application.usecases.documents.get import GetDocumentUseCase
from backend.application.usecases.documents.upload import UploadDocumentUseCase
from backend.application.usecases.events.attach_document import (
    AttachDocumentUseCase,
    UnAttachDocumentUseCase,
)
from backend.application.usecases.events.create import CreateEventUseCase
from backend.application.usecases.events.get import GetEventsUseCase, GetEventUseCase
from backend.application.usecases.events.update import UpdateEventUseCase
from backend.application.usecases.rsvp.set_status import SetRsvpStatusUseCase
from backend.application.usecases.users.create import CreateUserUseCase
from backend.application.usecases.users.get import GetUsersUseCase
from backend.application.usecases.users.me import GetMeUseCase
from backend.infrastructure.database.uow import UnitOfWorkImpl


class UsecasesProvider(Provider):
    scope = Scope.REQUEST

    # auth
    signin = provide(SignInUseCase)
    logout = provide(LogOutUseCase)

    # users
    me = provide(GetMeUseCase)
    get_all = provide(GetUsersUseCase)
    create_user = provide(CreateUserUseCase)

    # events
    get_events = provide(GetEventsUseCase)
    get_event = provide(GetEventUseCase)
    create_event = provide(CreateEventUseCase)
    update_event = provide(UpdateEventUseCase)
    send_notifications = provide(SendNotificationsUseCase)

    # rsvp
    set_rsvp_status = provide(SetRsvpStatusUseCase)

    # catalogs
    get_root_catalogs = provide(GetRootCatalogsUseCase)
    get_catalog = provide(GetCatalogUseCase)
    create_catalog = provide(CreateCatalogUseCase)
    delete_catalog = provide(DeleteCatalogUseCase)

    # documents
    get_document = provide(GetDocumentUseCase)
    upload_document = provide(UploadDocumentUseCase)
    create_document = provide(CreateDocumentUseCase)
    delete_document = provide(DeleteDocumentUseCase)

    # attach
    attach_document = provide(AttachDocumentUseCase)
    unattach_document = provide(UnAttachDocumentUseCase)

    # devices
    register_device = provide(RegisterDeviceUseCase)

    uow = provide(UnitOfWorkImpl, provides=UnitOfWork)

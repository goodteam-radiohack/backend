from backend.infrastructure.errors.gateways import ModelNotFoundError


class EventNotFoundError(ModelNotFoundError):
    message = "Event not found"

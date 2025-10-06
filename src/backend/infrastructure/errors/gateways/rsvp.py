from backend.infrastructure.errors.gateways import ModelNotFoundError


class RsvpNotFoundError(ModelNotFoundError):
    message = "RSVP Not found"

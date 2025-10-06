from backend.infrastructure.errors.gateways import ModelNotFoundError


class DeviceNotFoundError(ModelNotFoundError):
    message = "Device not found"

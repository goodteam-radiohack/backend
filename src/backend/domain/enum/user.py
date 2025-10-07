import enum


class UserRole(enum.StrEnum):
    DEPUTE = enum.auto()
    DEPUTE_HELPER = enum.auto()
    ADMIN = enum.auto()

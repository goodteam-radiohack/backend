import enum


class EventStatus(enum.StrEnum):
    SCHEDULED = enum.auto()
    IN_PROCESS = enum.auto()
    ENDED = enum.auto()
    CANCELED = enum.auto()

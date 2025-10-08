import enum


class EventStatus(enum.StrEnum):
    SCHEDULED = enum.auto()
    STARTING_SOON = enum.auto()
    IN_PROCESS = enum.auto()
    ENDED = enum.auto()
    CANCELED = enum.auto()


class EventVisibility(enum.StrEnum):
    PUBLIC = enum.auto()
    PRIVATE = enum.auto()

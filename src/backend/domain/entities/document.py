from backend.domain.entities.base import BaseEntity
from backend.domain.entities.user import UserEntity


class DocumentEntity(BaseEntity):
    id: int

    catalog_id: int | None

    name: str
    mime: str
    size: int

    storage_key: str
    checksum: str

    created_by_id: int
    created_by: UserEntity

    def is_author(self, user: UserEntity) -> bool:
        return user.id == self.created_by.id

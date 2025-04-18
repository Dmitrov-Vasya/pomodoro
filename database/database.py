from typing import Any

from sqlalchemy.orm import declared_attr, DeclarativeBase


class Base(DeclarativeBase):
    id: Any
    __name__: str
    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()




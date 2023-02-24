from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database.db import engine


class Base(DeclarativeBase):
    pass


class BarItem(Base):
    __tablename__ = "bar_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), index=True, unique=True)
    amount: Mapped[int] = mapped_column(Integer)


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

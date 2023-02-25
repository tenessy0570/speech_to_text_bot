from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.db import db_session
from database.db import engine


class Base(DeclarativeBase):
    pass


class BarItem(Base):
    __tablename__ = "bar_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), index=True, unique=True)
    amount: Mapped[int] = mapped_column(Integer)


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    bar_items = (
        ("Matua PN", 3),
        ("Norton Malbec", 2),
        ("Anakena CS", 2),
        ("RL Johnnie Wal.", 1),
        ("Martini Rosso", 1),
        ("Tanqueray", 3),
        ("Limoncello", 1)
    )

    with db_session as session:
        session.add_all(
            BarItem(name=item, amount=amount)
            for item, amount in bar_items
        )
        session.commit()

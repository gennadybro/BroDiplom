import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = "result"

    id = sq.Column(sq.Integer, primary_key = True)
    users = sq.Column(sq.Integer)
    partners = sq.Column(sq.String)
    view = sq.Column(sq.Boolean)


class Favourites(Base):
    __tablename__ = "favourites"

    id = sq.Column(sq.Integer, primary_key = True)
    users = sq.Column(sq.Integer)
    partners = sq.Column(sq.Integer)


def create_tables(engine):
    # Base.metadata.drop_all(engine)   ###  Убрать !
    Base.metadata.create_all(engine)


def drop_tables(engine):
    Base.metadata.drop.Parners(engine)

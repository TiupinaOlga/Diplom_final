import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData

# Схема ДБ
metadata = MetaData()
Base = declarative_base()


class Viewed(Base):
    __tablename__ = 'viewed'

    profile_id = sq.Column(sq.Integer, primary_key=True)
    worksheet_id = sq.Column(sq.Integer, unique=True)

    def __str__(self):
        return f'{self.worksheet_id}'


def drop_tables(engine):
    Base.metadata.drop_all(engine)


def create_tables(engine):
    Base.metadata.create_all(engine)

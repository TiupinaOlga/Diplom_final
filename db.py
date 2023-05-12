import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
# from config import DNS
from models import Viewed

"""Функция для вставки данных об анкете пользователя в бд"""


def insert_db(engine, profile_id, worksheet_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        print(profile_id)
        session.add(Viewed(profile_id=profile_id, worksheet_id=worksheet_id))
        session.commit()


"""Функция для поиска данных об анкете пользователя в бд"""


def get_worksheet(engine, worksheet_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query_pub = session.query(Viewed).filter(Viewed.worksheet_id == worksheet_id).all()
        if query_pub:
            return True
        else:
            return False


class DB_tools():
    def __init__(self, DNS):
        self.engine = sq.create_engine(DNS)

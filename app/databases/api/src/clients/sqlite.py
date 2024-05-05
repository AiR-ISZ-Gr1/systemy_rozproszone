import os
from sqlmodel import SQLModel, create_engine


SQLITE_FILE_NAME = os.environ["SQLITE_FILE_NAME"]
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

engine = create_engine(SQLITE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

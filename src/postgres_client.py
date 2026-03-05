import configparser
import uuid

from sqlalchemy import Table, Column, MetaData, String, DateTime, create_engine, UUID
from sqlalchemy.orm import sessionmaker

metadata = MetaData()

deployment_table = Table(
    "deployment_table",
    metadata,
    Column("id", UUID, default=uuid.uuid4(), primary_key=True),
    Column("db_name", String),
    Column("status", String),
    Column("username", String),
    Column("creation_time", DateTime)
)


def connect_to_postgres():

    config = configparser.ConfigParser()
    config.read("config.ini")

    engine = create_engine(f"postgresql+psycopg://{config['POSTGRES_CONNECTION']['user']}:"
                           f"{config['POSTGRES_CONNECTION']['password']}@"
                           f"{config['POSTGRES_CONNECTION']['host_name']}:"
                           f"{config['POSTGRES_CONNECTION']['port']}/"
                           f"{config['POSTGRES_CONNECTION']['db_name']}")

    session = sessionmaker(bind=engine)

    with session.begin():
        metadata.create_all(engine)

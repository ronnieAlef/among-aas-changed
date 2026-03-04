import uuid

from sqlalchemy import Table, Column, MetaData, Integer, Computed, Identity, String, func, DateTime, create_engine, UUID

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
    db_name = "oltp_db"
    user = "ronnie"
    password = "213248"
    host_name = "localhost"
    port = 5432

    engine = create_engine(f"postgresql+psycopg://{user}:{password}@{host_name}:{port}/{db_name}")

    metadata.create_all(engine)

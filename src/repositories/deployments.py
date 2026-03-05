from __future__ import annotations

import configparser
import datetime
import json
from uuid import UUID

from pydantic import parse_obj_as
from pymongo import MongoClient
from sqlalchemy import insert, select, Row, update, bindparam
from sqlalchemy.orm import sessionmaker

from src.models.deployment import Deployment
from src.postgres_client import connect_to_postgres, deployment_table
from src.requests.create_db_request import CreateDbRequest
from src.requests.rename_db_request import RenameDbRequest

config = configparser.ConfigParser()
config.read("config.ini")

engine = connect_to_postgres()
Session = sessionmaker(bind=engine)

mongo_connection = MongoClient(f"mongodb://"
                               f"{config['MONGO_CONNECTION']['user']}:"
                               f"{config['MONGO_CONNECTION']['password']}@"
                               f"{config['MONGO_CONNECTION']['host_name']}:"
                               f"{config['MONGO_CONNECTION']['port']}")


def create_new_mongo_db(create_db_request: CreateDbRequest) -> UUID:
    with mongo_connection.start_session() as session:
        with session.start_transaction():
            try:
                new_db = mongo_connection[create_db_request.db_name]
                new_db.mycoll.insert_one({"test": 'test'})
                generated_id = __write_deployment_to_postgres__(create_db_request)
                return generated_id

            except Exception as e:
                print("An error occurred:", e)
                session.abort_transaction()


def return_deployment_details(deployment_id: str):
    with Session.begin():

        stmt = select(deployment_table).where(deployment_table.c.id == deployment_id)
        result = engine.connect().execute(stmt).mappings().first()
        print(result)

        data = Deployment.model_validate(result)

        return data


def change_db_name(rename_db_request: RenameDbRequest, deployment_id: str) -> UUID:

    with engine.begin() as connection:
        stmt = (
            update(deployment_table)
            .where(deployment_table.c.id == deployment_id)
            .values(db_name=rename_db_request.db_name))

        result = connection.execute(stmt)
        generated_id = result.inserted_primary_key[0]
        return generated_id


def __write_deployment_to_postgres__(create_db_request: CreateDbRequest) -> UUID:
    with engine.begin() as connection:
        insertion = insert(deployment_table).values(db_name=create_db_request.db_name,
                                                    status='CREATED',
                                                    username=create_db_request.username,
                                                    creation_time=datetime.datetime.now())
        result = connection.execute(insertion)
        generated_id = result.inserted_primary_key[0]
        return generated_id

from __future__ import annotations

import configparser
import datetime
import json
from typing import Literal
from uuid import UUID

from pydantic import parse_obj_as
from pymongo import MongoClient
from sqlalchemy import insert, select, Row, update, bindparam
from sqlalchemy.orm import sessionmaker

from src.Errors import InvalidUsernameException
from src.headers.delete_db_header import DeleteDbHeader
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


def return_deployment_details(deployment_id: str) -> Deployment:
    with Session.begin():

        stmt = select(deployment_table).where(deployment_table.c.id == deployment_id)
        result = engine.connect().execute(stmt).mappings().first()
        print(result)

        data = Deployment.model_validate(result)

        return data


def change_db_name(rename_db_request: RenameDbRequest, deployment_id: str):
    # TODO: change name in mongo

    old_db_name = return_deployment_details(deployment_id).db_name

    source_db = mongo_connection[old_db_name]
    target_db = mongo_connection[rename_db_request.db_name]
    collection_names = source_db.list_collection_names()

    for collection_name in collection_names:
        source_collection = source_db[collection_name]
        target_collection = target_db[collection_name]

        documents = source_collection.find()

        # TODO: add logs
        doc_list = list(documents)
        if doc_list:
            target_collection.insert_many(doc_list)
            print(f"Copied {len(doc_list)} documents from '{collection_name}'")

    db_details = return_deployment_details(deployment_id)
    mongo_connection.drop_database(db_details.db_name)

    __change_db_name_postgres__(rename_db_request, deployment_id)


def delete_mongo_db(deployment_id: str, delete_db_header: DeleteDbHeader):
    with mongo_connection.start_session() as session:
        with session.start_transaction():
            try:
                db_details = return_deployment_details(deployment_id)

                if db_details.username == delete_db_header.username:
                    mongo_connection.drop_database(db_details.db_name)
                    __edit_deployment_status__("DELETED", deployment_id)
                    return db_details.id
                else:
                    #TODO: bubble it ap that the code didn't execute
                    raise InvalidUsernameException(delete_db_header.username)

            except Exception as e:
                print("An error occurred:", e)
                session.abort_transaction()


def __write_deployment_to_postgres__(create_db_request: CreateDbRequest) -> UUID:
    with engine.begin() as connection:
        insertion = insert(deployment_table).values(db_name=create_db_request.db_name,
                                                    status='CREATED',
                                                    username=create_db_request.username,
                                                    creation_time=datetime.datetime.now())
        result = connection.execute(insertion)
        generated_id = result.inserted_primary_key[0]
        return generated_id


def __edit_deployment_status__(status: Literal["DELETED", "CREATED"], deployment_id: str):
    with engine.begin() as connection:
        stmt = (
            update(deployment_table)
            .where(deployment_table.c.id == deployment_id)
            .values(status=status))

        connection.execute(stmt)


def __change_db_name_postgres__(rename_db_request: RenameDbRequest, deployment_id: str):
    with engine.begin() as connection:
        stmt = (
            update(deployment_table)
            .where(deployment_table.c.id == deployment_id)
            .values(db_name=rename_db_request.db_name))

        connection.execute(stmt)


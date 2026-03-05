import configparser
import datetime

from pymongo import MongoClient
from sqlalchemy import insert
from sqlalchemy.orm import Session, sessionmaker

from src.postgres_client import connect_to_postgres, deployment_table
from src.requests.create_db_request import CreateDbRequest

config = configparser.ConfigParser()
config.read("config.ini")


mongo_connection = MongoClient(f"mongodb://"
                         f"{config['MONGO_CONNECTION']['user']}:"
                         f"{config['MONGO_CONNECTION']['password']}@"
                         f"{config['MONGO_CONNECTION']['host_name']}:"
                         f"{config['MONGO_CONNECTION']['port']}")


def create_new_mongo_db(create_db_request: CreateDbRequest):

    with mongo_connection.start_session() as session:
        with session.start_transaction():
            try:
                new_db = mongo_connection[create_db_request.db_name]
                new_db.mycoll.insert_one({"test": 'test'})
                __write_deployment_to_postgres__(create_db_request)

            except Exception as e:
                print("An error occurred:", e)
                session.abort_transaction()


def __write_deployment_to_postgres__(create_db_request: CreateDbRequest):

    engine = connect_to_postgres()

    with engine.begin() as connection:
        insertion = insert(deployment_table).values(db_name=create_db_request.db_name,
                                                    status='CREATED',
                                                    username=create_db_request.username,
                                                    creation_time=datetime.datetime.now())
        connection.execute(insertion)



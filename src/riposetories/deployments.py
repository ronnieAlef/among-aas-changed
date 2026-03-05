import configparser

from pymongo import MongoClient
from sqlalchemy.orm import Session, sessionmaker

from src.requests.create_db_request import CreateDbRequest

config = configparser.ConfigParser()
config.read("config.ini")


connection = MongoClient(f"mongodb://"
                         f"{config['MONGO_CONNECTION']['user']}:"
                         f"{config['MONGO_CONNECTION']['password']}@"
                         f"{config['MONGO_CONNECTION']['host_name']}:"
                         f"{config['MONGO_CONNECTION']['port']}")


def create_new_mongo_db(create_db_request: CreateDbRequest):

    with connection.start_session() as session:
        with session.start_transaction():
            try:
                new_db = connection[create_db_request.db_name]
                new_db.mycoll.insert_one({"test": 'test'})
                __write_deployment_to_postgres(create_db_request)

            except Exception as e:
                print("An error occurred:", e)
                session.abort_transaction()


def __write_deployment_to_postgres(create_db_request: CreateDbRequest):



    pass



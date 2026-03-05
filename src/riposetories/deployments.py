from pymongo import MongoClient
from sqlalchemy.orm import Session, sessionmaker

from src.requests.create_db_request import CreateDbRequest

connection = MongoClient("mongodb://nraboy:password1234@localhost:27017")


def create_new_mongo_db(create_db_request: CreateDbRequest):

    with connection.start_session() as session:
        try:

            new_db = connection[create_db_request.db_name]
            new_db.mycoll.insert_one({"test": 'test'})
            print(connection.list_database_names())
            __write_deployment_to_postgres(create_db_request)
            session.commit_transaction()

        except Exception as e:
            print("An error occurred:", e)
            session.abort_transaction()


def __write_deployment_to_postgres(create_db_request: CreateDbRequest):


    pass



from pymongo import MongoClient
from pymongo.database import Collection, Database


class MongoDBManager:
    def __init__(self, con_string: str, database_name) -> None:
        self.client = MongoClient(con_string)
        self.db: Database = self.client[database_name]

    def __create_db(self, db_name: str) -> Database:
        return self.client[db_name]

    def create_collection(self, collection_name: str) -> Collection:
        return self.db.create_collection(collection_name)

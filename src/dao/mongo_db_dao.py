import json
import os

from dotenv import load_dotenv
from pymongo import errors, MongoClient

from dao.dao import DAO


class MongoDbDAO(DAO):

    def __init__(self) -> None:
        super().__init__()

        self.__port: int = 27017
        self.__connection: MongoClient = self.create_connection(
            username=os.getenv('USERNAME'),
            password=os.getenv('PASSWORD')
        )

    def create_connection(self, **kwargs):
        # TODO - Docstring
        try:
            connection = MongoClient(
                host=f'mongo:{self.__port}',
                serverSelectionTimeoutMS=3000,  # 3 second timeout
                username=kwargs['username'],
                password=kwargs['password'],
            )

        except errors.ServerSelectionTimeoutError as err:
            connection = None

            print('pymongo ERROR:', err)

            exit(-1)

        return connection

    def read_data(self, **kwargs):
        # TODO - Docstring
        collection = self.__connection[kwargs['database']][kwargs['collection']]
    
        for entry in collection.find():
            print(entry)

    def insert_data(self, **kwargs):
        # TODO - Docstring

        try:
            self.__connection[kwargs['database']][kwargs['collection']].insert_many(kwargs['data'])

        except errors.BulkWriteError as bwe:
            print(bwe.details)
            raise

    def update_data(self, **kwargs):
        # TODO - Docstring
        pass

    def delete_data(self, **kwargs):
        # TODO - Docstring
        pass

    def close_connection(self, **kwargs):
        # TODO - Docstring
        self.__connection.close()

    def populate_database(self, data_folder: str) -> None:
        # TODO - Docstring

        for file in os.listdir(data_folder):
            data = []
            with open(os.path.join(data_folder, file)) as json_file:
                for line in json_file:
                    data.append(json.loads(line))

            self.insert_data(
                database='ASOS_2022',
                collection=file.split('.')[0],
                data=data
            )

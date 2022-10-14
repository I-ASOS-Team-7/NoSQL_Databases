import json
import os
from typing import List, Union

from pymongo import errors, MongoClient

from dao.dao import DAO


class MongoDbDAO(DAO):

    """Represents MongoDB Database Access Object."""

    def __init__(self) -> None:
        """Initializes the MongoDbDAO Class."""
        super().__init__()

        self.__port: int = 27017
        self.__connection: MongoClient = self.create_connection(
            username=os.getenv('USERNAME'),
            password=os.getenv('PASSWORD')
        )

    def create_connection(self, **kwargs: str) -> MongoClient:
        """Creates new MongoDB Connection.

        Args:
            **kwargs (str): Keyword Arguments ('username' and 'password' 
            expected).

        Returns:
            MongoClient: New MongoDB Connection.
        """
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

    def read_data(self, **kwargs: str) -> None:
        """Reads every entry in Collection.

        Args:
            **kwargs (str): Keyword Arguments ('database' and 'collection' 
            expected).
        """
        collection = self.__connection[kwargs['database']][kwargs['collection']]
    
        for entry in collection.find():
            print(entry)

    def insert_data(self, **kwargs: Union[str, List[dict]]) -> None:
        """Inserts entries in Collection.

        Args:
            **kwargs (Union[str, List[dict]]): Keyword Arguments ('database',
            'collection' and 'data' expected).
        """
        try:
            (
                self.__connection[kwargs['database']][kwargs['collection']]
                    .insert_many(kwargs['data'])
            )

        except errors.BulkWriteError as bwe:
            print(bwe.details)
            raise

    def update_data(self, **kwargs: Union[str, List[dict]]) -> None:
        """Updates entries in Collection.

        Args:
            **kwargs (Union[str, List[dict]]): Keyword Arguments ('database',
            'collection', 'old_values' and 'new_values' expected).
        """
        (
            self.__connection[kwargs['database']][kwargs['collection']]
                .update_many(
                    kwargs['old_values'], 
                    kwargs['new_values']
                )
        )

    def delete_data(self, **kwargs: str) -> None:
        """Removes every entry from Collection.

        Args:
            **kwargs (str): Keyword Arguments ('database' and 'collection' 
            expected).
        """
        (
            self.__connection[kwargs['database']][kwargs['collection']]
                .delete_many({})
        )

    def close_connection(self):
        """Closes MongoDB Connection."""
        self.__connection.close()

    def populate_database(self, data_folder: str) -> None:
        """Populates MongoDB Database from JSON Files in Data Folder.

        Args:
            data_folder (str): Data Folder Path.
        """
        for file in os.listdir(data_folder):
            data = []
            with open(os.path.join(data_folder, file)) as json_file:
                for line in json_file:
                    data.append(json.loads(line))

            self.insert_data(
                database=os.getenv('DB_NAME'),
                collection=file.split('.')[0],
                data=data
            )

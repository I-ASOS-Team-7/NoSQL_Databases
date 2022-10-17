import json
import os
import time
from typing import List, Union

from pymongo import errors, MongoClient

from dao.dao import DAO
from stats.statistics import Statistics


class MongoDbDAO(DAO):

    """Represents MongoDB Data Access Object."""

    def __init__(self, statistics: Statistics) -> None:
        """Initializes the MongoDbDAO Class.

        Args:
            statistics (Statistics): Database Testing Statistics Object.
        """
        super().__init__()

        self.__database_type: str = 'MongoDB'
        self.__port: int = 27017
        self.__connection: MongoClient = self.create_connection(
            username=os.getenv('USERNAME'),
            password=os.getenv('PASSWORD')
        )
        self.__statistics: Statistics = statistics

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
                host=f"mongodb://localhost:{self.__port}/",
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
        collection = self.__connection[kwargs['database']
                                       ][kwargs['collection']]
        
        start_time = time.time()

        for entry in collection.find():
            print(entry)

        self.__statistics.add_execution_time(
            database_type=self.__database_type,
            database=kwargs['database'],
            dataset=kwargs['collection'],
            action='read',
            time=time.time() - start_time
        )


    def insert_data(self, **kwargs: Union[str, List[dict]]) -> None:
        """Inserts entries to Collection.

        Args:
            **kwargs (Union[str, List[dict]]): Keyword Arguments ('database',
            'collection' and 'data' expected).
        """
        try:
            start_time = time.time()
            (
                self.__connection[kwargs['database']][kwargs['collection']]
                .insert_many(kwargs['data'])
            )
            self.__statistics.add_execution_time(
                database_type=self.__database_type,
                database=kwargs['database'],
                dataset=kwargs['collection'],
                action='insert',
                time=time.time() - start_time
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
        start_time = time.time()
        (
            self.__connection[kwargs['database']][kwargs['collection']]
            .update_many(
                kwargs['old_values'],
                kwargs['new_values']
            )
        )
        self.__statistics.add_execution_time(
            database_type=self.__database_type,
            database=kwargs['database'],
            dataset=kwargs['collection'],
            action='update',
            time=time.time() - start_time
        )

    def delete_data(self, **kwargs: str) -> None:
        """Removes every entry from Collection.

        Args:
            **kwargs (str): Keyword Arguments ('database' and 'collection' 
            expected).
        """
        start_time = time.time()
        (
            self.__connection[kwargs['database']][kwargs['collection']]
            .delete_many({})
        )
        self.__statistics.add_execution_time(
            database_type=self.__database_type,
            database=kwargs['database'],
            dataset=kwargs['collection'],
            action='delete',
            time=time.time() - start_time
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

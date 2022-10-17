import json
import os
import time

from redis import Redis
from redis.commands.json.path import Path

from dao.dao import DAO
from stats.statistics import Statistics

class RedisDAO(DAO):

    """Represents Redis Database Access Object."""

    def __init__(self, statistics: Statistics) -> None:
        """Initializes the RedisDAO Class.
        
        Args:
            statistics (Statistics): Database Testing Statistics Object.
        """
        super().__init__()

        self.__database_type: str = 'Redis'
        self.__port: int = 6379
        self.__connection: Redis = self.create_connection()
        self.__statistics: Statistics = statistics

    def create_connection(self, **kwargs):
        """Creates new Redis Connection.

        Returns:
            Redis: New Redis Connection.
        """
        return Redis(
            host='localhost',
            port=self.__port,
            decode_responses=True
        )

    def read_data(self, **kwargs):
        """Reads every Document from the Database with a specific ID prefix.

        Args:
            **kwargs (str): Keyword Arguments ('database' and 'collection' 
            expected).
        """
        database_name = '_'.join(
            [kwargs['database'], kwargs['collection']]
        ).lower()

        start_time = time.time()

        for key in self.__connection.scan_iter(f'{database_name}*'):
            print(self.__connection.json().get(key))

        self.__statistics.add_execution_time(
            database_type=self.__database_type,
            database=kwargs['database'],
            dataset=kwargs['collection'],
            action='read',
            time=time.time() - start_time
        )

    def insert_data(self, **kwargs):
        """Inserts key value pair to the Redis database.

        Args:
            **kwargs (str): Keyword Arguments ('key' and 'data' expected).
        """        
        self.__connection.json().set(
            kwargs['key'], Path.root_path(), kwargs['data']
        )

    def update_data(self, **kwargs):
        """Updates value for a specific key.

        Args:
            **kwargs (Union[str, List[str]]): Keyword Arguments ('database', 
            'collection', 'doc_ids', 'key' and 'new_value' expected).
        """
        database_name = '_'.join(
            [kwargs['database'], kwargs['collection']]
        ).lower()

        start_time = time.time()

        doc_ids = kwargs['doc_ids']
        if doc_ids is None or len(doc_ids) == 0:
            doc_ids = []

            for doc_id in self.__connection.scan_iter(f"{database_name}*"):
                doc_ids.append(doc_id)

        for doc_id in doc_ids:
            document = self.__connection.json().get(doc_id)
            document[kwargs['key']] = kwargs['new_value']

            self.__connection.json().set(
                doc_id, Path.root_path(), document
            )

        self.__statistics.add_execution_time(
            database_type=self.__database_type,
            database=kwargs['database'],
            dataset=kwargs['collection'],
            action='update',
            time=time.time() - start_time
        )

    def delete_data(self, **kwargs):
        """Removes every Document from Database with specific ID prefix.

        Args:
            **kwargs (str): Keyword Arguments ('database' and'collection' 
            expected).
        """
        database_name = '_'.join(
            [kwargs['database'], kwargs['collection']]
        ).lower()

        start_time = time.time()

        for key in self.__connection.keys(f'{database_name}*'):
            self.__connection.delete(key)

        self.__statistics.add_execution_time(
            database_type=self.__database_type,
            database=kwargs['database'],
            dataset=kwargs['collection'],
            action='delete',
            time=time.time() - start_time
        )
        
    def close_connection(self):
        """Closes Redis connection.
        
        No need to close the database, Redis handles closing the database 
        automatically for the client.
        """
        pass

    def populate_database(self, data_folder: str) -> None:
        """Populates Redis Database from JSON Files in Data Folder.

        Args:
            data_folder (str): Data Folder Path.
        """
        for file in os.listdir(data_folder):
            start_time = time.time()

            with open(os.path.join(data_folder, file)) as json_file:
                for line in json_file:
                    data=json.loads(line)

                    key = '_'.join(
                        [
                            os.getenv('DB_NAME'),
                            file.split('.')[0],
                            str(data['id'])
                        ]
                    ).lower()

                    self.insert_data(
                        database=os.getenv('DB_NAME'),
                        collection=file.split('.')[0],
                        key=key,
                        data=data
                    )

            self.__statistics.add_execution_time(
                database_type=self.__database_type,
                database=os.getenv('DB_NAME'),
                dataset=file.split('.')[0],
                action='insert',
                time=time.time() - start_time
            )

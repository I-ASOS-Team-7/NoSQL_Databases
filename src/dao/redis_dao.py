from dao.dao import DAO
import redis
from redis.commands.json.path import Path
from stats.statistics import Statistics
import os
import json
import time

class RedisDAO(DAO):

    """Represents Redis Database Access Object."""

    def __init__(self, statistics: Statistics) -> None:
        """Initializes the RedisDAO Class.
        
        Args:
            statistics (Statistics): Database Testing Statistics Object.
        """
        super().__init__()
        self.__port: int = 6379
        self.__connection = self.create_connection(
            #username=os.getenv('USERNAME'),
            #password=os.getenv('PASSWORD')
            password='MDNcVb924a'
        )
        self.__statistics: Statistics = statistics

    def create_connection(self, **kwargs):
        """Creates new Redis Connection.

        Args:
            **kwargs (str): Keyword Arguments ('username' and 'password' 
            expected).

        Returns:
            Redis: New Redis Connection.
        """
        r = redis.Redis(
            host='redis-redisjson',
            port=self.__port,
            #username='',#kwargs['username'], 
            #password=''#kwargs['password'], 
            decode_responses=True)
        return r

    def read_data(self, **kwargs):
        result = self.__connection.json().get(kwargs['key'])
        print(result)

    def insert_data(self, **kwargs):
        """Inserts key value pair in the redis database.

        Args:
            **kwargs (str): Keyword Arguments ('key' and 'data' 
            expected).
        """
        start_time = time.time()
        self.__connection.json().set(kwargs['key'], Path.root_path(), kwargs['data'])
        self.__statistics.add_insert_time(
            database_type='Redis',
            database='ASOS_2022',
            dataset='',
            time=time.time() - start_time
        )

    def update_data(self, **kwargs):
        """Updates value for a specific key.

        Args:
            **kwargs (str): Keyword Arguments ('key',
            and 'data', expected).
        """
        self.__connection.json().set(kwargs['key'], Path.root_path(), kwargs['data'])
        pass

    def delete_data(self, **kwargs):
        """Removes every key from database.

        Args: None
        """
        for key in self.__connection.keys('prefix:*'):
            self.__connection.delete(key)
        

    def close_connection(self):
        """
        No need to close the database, redis.Redis handles closing the database automatically for the client.
        """
        pass

    def populate_database(self, data_folder: str) -> None:
        """Populates Redis Database from JSON Files in Data Folder.

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
                key='adsadadsad',
                data=data
            )

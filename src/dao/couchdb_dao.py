import json
import os
import time

from couchdb import Server

from dao.dao import DAO
from stats.statistics import Statistics


class CouchDbDAO(DAO):

    """Represents CouchDB Data Access Object."""

    def __init__(self, statistics: Statistics) -> None:
        """Initializes the CouchDbDAO Class.

        Args:
            statistics (Statistics): Database Testing Statistics Object.
        """
        super().__init__()
        
        self.__database_type: str = 'CouchDB'
        self.__connection: Server = self.create_connection(
            username=os.getenv('ASOS_USERNAME'),
            password=os.getenv('PASSWORD')
        )
        self.__statistics: Statistics = statistics

    def create_connection(self, **kwargs) -> Server:
        """Creates new CouchDB Connection.

        Args:
            **kwargs (str): Keyword Arguments ('username' and 'password'
            expected).

        Returns:
            Server: New CouchDB Connection.
        """
        server = Server()
        server.resource.credentials = (kwargs['username'], kwargs['password'])

        return server

    def read_data(self, **kwargs) -> None:
        """Reads every entry in Database.

        Args:
            **kwargs (str): Keyword Arguments ('database' and 'collection'
            expected).
        """
        database_name = (
            '_'.join([kwargs['database'], kwargs['collection']]).lower()
        )

        start_time = time.time()

        for _id in self.__connection[database_name]:
            print(self.__connection[database_name][_id])

        self.__statistics.add_execution_time(
            database_type=self.__database_type,
            database=kwargs['database'],
            dataset=kwargs['collection'],
            action='read',
            time=time.time() - start_time
        )


    def insert_data(self, **kwargs) -> None:
        """Inserts Document to Database.

        Args:
            **kwargs (Union[str, dict]): Keyword Arguments ('database',
            'collection' and 'data' expected).
        """
        self.__connection[
            '_'.join([kwargs['database'], kwargs['collection']]).lower()
        ].save(kwargs['data'])

    def update_data(self, **kwargs) -> None:
        """Updates Documents in Database.

        Args:
            **kwargs (Union[str, List[dict]]): Keyword Arguments ('database',
            'collection', 'key' and 'new_value' expected).
        """
        database_name = (
            '_'.join([kwargs['database'], kwargs['collection']]).lower()
        )

        start_time = time.time()

        doc_ids = kwargs['doc_ids']
        if doc_ids is None or len(doc_ids) == 0:
            doc_ids = []

            for _id in self.__connection[database_name]:
                doc_ids.append(_id)

        for doc_id in doc_ids:
            document = self.__connection[database_name][doc_id]
            document[kwargs['key']] = kwargs['new_value']
            self.__connection[database_name].save(document)

        self.__statistics.add_execution_time(
            database_type=self.__database_type,
            database=kwargs['database'],
            dataset=kwargs['collection'],
            action='update',
            time=time.time() - start_time
        )

    def delete_data(self, **kwargs):
        """Removes every Document from Database.

        Args:
            **kwargs (str): Keyword Arguments ('database' and 'collection' 
            expected).
        """
        start_time = time.time()
        database_name = (
            '_'.join([kwargs['database'], kwargs['collection']]).lower()
        )

        self.__connection.delete(database_name)
        self.__connection.create(database_name)

        self.__statistics.add_execution_time(
            database_type=self.__database_type,
            database=kwargs['database'],
            dataset=kwargs['collection'],
            action='delete',
            time=time.time() - start_time
        )

    def close_connection(self):
        """Closes CouchDB Connection."""
        self.__connection = None

    def populate_database(self, data_folder: str) -> None:
        """Populates CouchDB Database from JSON Files in Data Folder.

        Args:
            data_folder (str): Data Folder Path.
        """
        for file in os.listdir(data_folder):
            start_time = time.time()

            database_name = (
                '_'.join([os.getenv('DB_NAME'), file.split('.')[0]]).lower()
            )

            if database_name not in self.__connection:
                self.__connection.create(database_name)

            with open(os.path.join(data_folder, file)) as json_file:
                for line in json_file:
                    self.insert_data(
                        database=os.getenv('DB_NAME'),
                        collection=file.split('.')[0],
                        data=json.loads(line)
                    )

            self.__statistics.add_execution_time(
                database_type=self.__database_type,
                database=os.getenv('DB_NAME'),
                dataset=file.split('.')[0],
                action='insert',
                time=time.time() - start_time
            )

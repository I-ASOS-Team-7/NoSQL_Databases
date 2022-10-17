from neo4j import GraphDatabase

from dao.dao import DAO


class Neo4jDAO(DAO):

	def __init__(self) -> None:
		super().__init__()

		self.__port: int = 7687
		self.__connection = self.create_connection()
		print(self.__connection)

	def create_connection(self, **kwargs):
		# TODO - Docstring
		return (
			GraphDatabase.driver(uri=f'neo4j://localhost:{self.__port}')
						 .session()
		)

	def read_data(self, **kwargs):
		# TODO - Docstring
		pass

	def insert_data(self, **kwargs):
		# TODO - Docstring
		pass

	def update_data(self, **kwargs):
		# TODO - Docstring
		pass

	def delete_data(self, **kwargs):
		# TODO - Docstring
		pass

	def close_connection(self):
		# TODO - Docstring
		pass

# SOURCE: https://towardsdatascience.com/create-a-graph-database-in-neo4j-using-python-4172d40f89c4

import os
import time
from typing import Tuple

import pandas as pd

from dao.dao import DAO
from dao.neo4j_connection import Neo4jConnection
from stats.statistics import Statistics
from utils.archive_utils import load_and_clean_archive_data


class Neo4jDAO(DAO):

	"""Represents Neo4j Data Access Object."""

	def __init__(self) -> None:
		"""Initializes the Neo4jDAO Class."""
		super().__init__()

		self.__port: int = 7687
		self.__connection = self.create_connection(
			username=os.getenv('ASOS_USERNAME'),
            password=os.getenv('PASSWORD')
		)

	def create_connection(self, **kwargs):
		"""Creates new Neo4j Connection.

        Returns:
            Neo4jConnection: New Neo4j Connection.
        """
		return Neo4jConnection(
			uri=f'neo4j://localhost:{self.__port}/',
		)

	def read_data(self, **kwargs):
		"""Reads every entry in Graph."""
		pass

	def insert_data(self, **kwargs):
		"""Inserts data to Graph."""
		statistics = Statistics(iterations=1)

		start_time = time.time()
		self.__add_categories(self.__categories)
		statistics.add_execution_time(
			database_type='Neo4j',
			database='Default',
			dataset='Categories',
			action='insert',
			time=time.time() - start_time
		)

		start_time = time.time()
		self.__add_authors(self.__authors)
		statistics.add_execution_time(
			database_type='Neo4j',
			database='Default',
			dataset='Authors',
			action='insert',
			time=time.time() - start_time
		)

		start_time = time.time()
		self.__add_papers(self.__data)
		statistics.add_execution_time(
			database_type='Neo4j',
			database='Default',
			dataset='Papers',
			action='insert',
			time=time.time() - start_time
		)			
		
		statistics.display_statistics()
		statistics.export_plots()

	def update_data(self, **kwargs):
		"""Updates data in Graph."""
		pass

	def delete_data(self, **kwargs):
		"""Deletes every data in every Graph."""
		query = '''
				MATCH (n)
				DETACH DELETE n
				'''

		self.__connection.query(query)

	def close_connection(self):
		"""Closes Neo4j Connection."""
		self.__connection.close()
		self.__connection = None

	def __create_tables(self) -> None:
		self.__connection.query('CREATE CONSTRAINT papers IF NOT EXISTS ON (p:Paper) ASSERT p.id IS UNIQUE')
		self.__connection.query('CREATE CONSTRAINT authors IF NOT EXISTS ON (a:Author) ASSERT a.name IS UNIQUE')
		self.__connection.query('CREATE CONSTRAINT categories IF NOT EXISTS ON (c:Category) ASSERT c.category IS UNIQUE')

	def __add_categories(self, categories):
        # Adds category nodes to the Neo4j graph.
		query = '''
				UNWIND $rows AS row
				MERGE (c:Category {category: row.category})
				RETURN count(*) as total
				'''
		return self.__connection.query(query, parameters = {'rows':categories.to_dict('records')})


	def __add_authors(self, rows, batch_size=10000):
		# Adds author nodes to the Neo4j graph as a batch job.
		query = '''
				UNWIND $rows AS row
				MERGE (:Author {name: row.author})
				RETURN count(*) as total
				'''
		return self.__insert_data(query, rows, batch_size)

	def __add_papers(self, rows, batch_size=5000):
		# Adds paper nodes and (:Author)--(:Paper) and 
		# (:Paper)--(:Category) relationships to the Neo4j graph as a 
		# batch job.
		
		query = '''
		UNWIND $rows as row
		MERGE (p:Paper {id:row.id}) ON CREATE SET p.title = row.title
		
		// connect categories
		WITH row, p
		UNWIND row.category_list AS category_name
		MATCH (c:Category {category: category_name})
		MERGE (p)-[:IN_CATEGORY]->(c)
		
		// connect authors
		WITH distinct row, p // reduce cardinality
		UNWIND row.cleaned_authors_list AS author
		MATCH (a:Author {name: author})
		MERGE (a)-[:AUTHORED]->(p)
		RETURN count(distinct p) as total
		'''
		
		return self.__insert_data(query, rows, batch_size)


	def __insert_data(self, query, rows, batch_size = 10000):
		# Function to handle the updating the Neo4j database in batch mode.
		
		total = 0
		batch = 0
		start = time.time()
		result = None
		
		while batch * batch_size < len(rows):

			res = self.__connection.query(
				query, 
				parameters = {'rows': rows[batch*batch_size:(batch+1)*batch_size].to_dict('records')}
			)
			total += res[0]['total']
			batch += 1
			result = {"total":total, 
					"batches":batch, 
					"time":time.time()-start}
			print(result)

		return result

	def __process_data(
		self, 
		data: pd.DataFrame
	) -> Tuple[pd.DataFrame, pd.DataFrame]:
		categories = pd.DataFrame(data[['category_list']])
		categories.rename(
			columns={'category_list':'category'},
			inplace=True
		)
		categories = (
			categories.explode('category').drop_duplicates(subset=['category'])
		)

		authors = pd.DataFrame(data[['cleaned_authors_list']])
		authors.rename(
			columns={'cleaned_authors_list':'author'},
			inplace=True
		)
		authors=authors.explode('author').drop_duplicates(subset=['author'])

		return categories, authors

	def populate_database(self, data_folder: str) -> None:
		"""Populates Neo4j Database from JSON Files in Data Folder.

        Args:
            data_folder (str): Data Folder Path.
        """
		for file in os.listdir(data_folder):
			self.__create_tables()
			self.__data = load_and_clean_archive_data(
				file_path=os.path.join(
					data_folder,
					file
				),
				lines=100000
			)		
			self.__categories, self.__authors = self.__process_data(
				data=self.__data
			)
			
			self.insert_data()

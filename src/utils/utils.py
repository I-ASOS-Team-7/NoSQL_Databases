import os
from typing import Optional

from dao.couchdb_dao import CouchDbDAO
from dao.mongo_db_dao import MongoDbDAO
from dao.neo4j_dao import Neo4jDAO
from dao.redis_dao import RedisDAO
from stats.statistics import Statistics


def run_couchdb(
	statistics: Statistics,
	iterations: Optional[int] = 10
) -> None:
	"""Run basic CouchDB DAO Functionalities.

	Args:
		statistics (Statistics): Database Testing Statistics Object.
		iterations (Optional[int]): Number of repetition. Defaults to 10.
	"""
	couchdb_dao = CouchDbDAO(statistics)

	counchdb_path = os.path.join(os.getcwd(), 'data', 'json_data')
	collections = sorted(os.listdir(counchdb_path))

	for iteration in range(iterations):
		couchdb_dao.populate_database(data_folder=counchdb_path)

		for collection in collections:
			print(collection.split('.')[0])
			couchdb_dao.read_data(
				database=os.getenv('DB_NAME'),
				collection=collection.split('.')[0]
			)

			if collection == 'data.json':
				couchdb_dao.update_data(
					database=os.getenv('DB_NAME'),
					collection=collection.split('.')[0],
					doc_ids=[],
					key='address',
					new_value=f'Docker_{iteration}'
				)
	
		for collection in collections:
			couchdb_dao.delete_data(
				database=os.getenv('DB_NAME'),
				collection=collection.split('.')[0]
			)

	couchdb_dao.close_connection()


def run_mongodb(
	statistics: Statistics,
	iterations: Optional[int] = 10
) -> None:
	"""Run basic MongoDB DAO Functionalities.

	Args:
		statistics (Statistics): Database Testing Statistics Object.
		iterations (Optional[int]): Number of repetition. Defaults to 10.
	"""
	mongodb_dao = MongoDbDAO(statistics)

	mongodb_path = os.path.join(os.getcwd(), 'data', 'json_data')
	collections = sorted(os.listdir(mongodb_path))

	for iteration in range(iterations):
		for collection in collections:
			mongodb_dao.delete_data(
				database=os.getenv('DB_NAME'),
				collection=collection.split('.')[0]
			)

		mongodb_dao.populate_database(
			data_folder=mongodb_path
		)

		for collection in collections:
			mongodb_dao.read_data(
				database=os.getenv('DB_NAME'),
				collection=collection.split('.')[0]
			)

		update_mapping = {
			'data': {
				'old_values': {'name': {'$regex': '.'}},
				'new_values': {'$set': {'address': f'Docker_{iteration}'}}
			}
		}

		for key, value in update_mapping.items():
			mongodb_dao.update_data(
				database=os.getenv('DB_NAME'),
				collection=key,
				old_values=value['old_values'],
				new_values=value['new_values']
			)

	mongodb_dao.close_connection()


def run_neo4j() -> None:
	"""Run basic Neo4j DAO Functionalities."""
	neo4j_path = os.path.join(os.getcwd(), 'data', 'archive')

	neo4j_dao = Neo4jDAO()

	neo4j_dao.populate_database(
		data_folder=neo4j_path
	)

	neo4j_dao.delete_data()


def run_redis(
	statistics: Statistics,
	iterations: Optional[int] = 10
) -> None:
	"""Run basic Redis DAO Functionalities.

	Args:
		statistics (Statistics): Database Testing Statistics Object.
		iterations (Optional[int]): Number of repetition. Defaults to 10.
	"""
	redis_dao = RedisDAO(statistics)

	redis_path = os.path.join(os.getcwd(), 'data', 'json_data')
	collections = sorted(os.listdir(redis_path))

	for iteration in range(iterations):
		for collection in collections:
			redis_dao.delete_data(
				database=os.getenv('DB_NAME'),
				collection=collection.split('.')[0]
			)

		redis_dao.populate_database(data_folder=redis_path)

		for collection in collections:
			redis_dao.read_data(
				database=os.getenv('DB_NAME'),
				collection=collection.split('.')[0]
			)

		redis_dao.update_data(
			database=os.getenv('DB_NAME'),
			collection='data',
			doc_ids=[],
			key='address',
			new_value=f'Docker_{iteration}'
		)

	redis_dao.close_connection()

import os
from typing import Optional
from dao.couchdb_dao import CouchDbDAO


from dao.mongo_db_dao import MongoDbDAO
from stats.statistics import Statistics


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

	mongodb_path = os.path.join(os.getcwd(), 'data', 'mongodb_data')
	collections = sorted(os.listdir(mongodb_path))

	for _ in range(iterations):
		for collection in collections:
			mongodb_dao.delete_data(
				database=os.getenv('DB_NAME'),
				collection=collection.split('.')[0]
			)

		mongodb_dao.populate_database(
			data_folder=mongodb_path
		)

		# for collection in collections:
		#     mongodb_dao.read_data(
		#         database=os.getenv('DB_NAME'),
		#         collection=collection.split('.')[0]
		#     )

		update_mapping = {
			'data': {
				'old_values': {'name': {'$regex': '^V'}},
				'new_values': {'$set': {'address': 'Docker'}}
			}
		}

		for key, value in update_mapping.items():
			mongodb_dao.update_data(
				database=os.getenv('DB_NAME'),
				collection=key,
				old_values=value['old_values'],
				new_values=value['new_values']
			)

		# mongodb_dao.read_data(
		#     database=os.getenv('DB_NAME'),
		#     collection='data'
		# )

	mongodb_dao.close_connection()


def run_couchdb(
	statistics: Statistics,
	iterations: Optional[int] = 10
) -> None:
	# TODO - Docstring
	couchdb_dao = CouchDbDAO(statistics)

	counchdb_path = os.path.join(os.getcwd(), 'data', 'mongodb_data')
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

				couchdb_dao.read_data(
					database=os.getenv('DB_NAME'),
					collection=collection.split('.')[0]
				)

		for collection in collections:
		    couchdb_dao.delete_data(
		        database=os.getenv('DB_NAME'),
		        collection=collection.split('.')[0]
		    )

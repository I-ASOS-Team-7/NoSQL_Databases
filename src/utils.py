import os

from dao.mongo_db_dao import MongoDbDAO


def run_mongodb() -> None:
    """Run basic MongoDB DAO Functionalities."""
    mongodb_dao = MongoDbDAO()

    mongodb_path = os.path.join(os.getcwd(), 'data', 'mongodb_data')

    for collection in sorted(os.listdir(mongodb_path)):
        mongodb_dao.delete_data(
            database=os.getenv('DB_NAME'),
            collection=collection.split('.')[0]
        )

    mongodb_dao.populate_database(
        data_folder=mongodb_path
    )

    for collection in sorted(os.listdir(mongodb_path)):
        mongodb_dao.read_data(
            database=os.getenv('DB_NAME'),
            collection=collection.split('.')[0]
        )

    mongodb_dao.update_data(
        database=os.getenv('DB_NAME'),
        collection='data',
        old_values={'name' : {'$regex': '^V'}},
        new_values={'$set': { 'address': 'Docker' }}
    )

    mongodb_dao.read_data(
        database=os.getenv('DB_NAME'),
        collection='data'
    )    

    mongodb_dao.close_connection()
import os

from dotenv import load_dotenv

from dao.mongo_db_dao import MongoDbDAO


if __name__ == '__main__':
    load_dotenv()

    mongodb_dao = MongoDbDAO()

    # mongodb_dao.insert_data(
    #     database='mydatabase',
    #     collection='customers',
    #     data=[
    #         {'name': 'Amy', 'address': 'Apple st 652'},
    #         {'name': 'Hannah', 'address': 'Mountain 21'},
    #         {'name': 'Michael', 'address': 'Valley 345'},
    #         {'name': 'Sandy', 'address': 'Ocean blvd 2'},
    #         {'name': 'Betty', 'address': 'Green Grass 1'},
    #         {'name': 'Richard', 'address': 'Sky st 331'},
    #         {'name': 'Susan', 'address': 'One way 98'},
    #         {'name': 'Vicky', 'address': 'Yellow Garden 2'},
    #         {'name': 'Ben', 'address': 'Park Lane 38'},
    #         {'name': 'William', 'address': 'Central st 954'},
    #         {'name': 'Chuck', 'address': 'Main Road 989'},
    #         {'name': 'Viola', 'address': 'Sideway 1633'}
    #     ]
    # )

    # mongodb_dao.read_data(database='mydatabase', collection='customers')

    mongodb_dao.populate_database(
        data_folder=os.path.join(os.getcwd(), 'data', 'mongodb_data')
    )

    for collection in os.listdir(os.path.join(os.getcwd(), 'data', 'mongodb_data')):

        print(f"main: {collection.split('.')[0]}")
        mongodb_dao.read_data(
            database='ASOS_2022',
            collection=collection.split('.')[0]
        )

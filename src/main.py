import os

from dotenv import load_dotenv
from pymongo import errors, MongoClient

load_dotenv()

PORT = 27017
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# use a try-except indentation to catch MongoClient() errors
try:

    # try to instantiate a client instance
    client = MongoClient(
        # host=[str(DOMAIN) + ":" + str(PORT)],
        host=f"mongo:{PORT}",
        serverSelectionTimeoutMS=3000,  # 3 second timeout
        username=USERNAME,
        password=PASSWORD,
    )

    # print the version of MongoDB server if connection successful
    print("server version:", client.server_info()["version"])

    mydb = client["mydatabase"]
    mycol = mydb["customers"]

    mydict = {"name": "John", "address": "Highway 37"}

    x = mycol.insert_one(mydict)

    print(f"Inserted: {mycol.find_one()}")

    # get the database_names from the MongoClient()
    database_names = client.list_database_names()

except errors.ServerSelectionTimeoutError as err:
    # set the client and DB name list to 'None' and `[]` if exception
    client = None
    database_names = []

    # catch pymongo.errors.ServerSelectionTimeoutError
    print("pymongo ERROR:", err)

print("\ndatabases:", database_names)

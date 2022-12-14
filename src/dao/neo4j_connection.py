# SOURCE: https://towardsdatascience.com/create-a-graph-database-in-neo4j-using-python-4172d40f89c4

from neo4j import GraphDatabase

class Neo4jConnection:
    
    def __init__(self, uri):
        self.__uri = uri
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri)
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response
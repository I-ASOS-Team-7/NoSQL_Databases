from dao.dao import DAO


class Neo4jDAO(DAO):

    def __init__(self) -> None:
        super().__init__()

    def create_connection(self, **kwargs):
        # TODO - Docstring
        pass

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

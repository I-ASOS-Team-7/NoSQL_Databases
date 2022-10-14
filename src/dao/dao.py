from abc import ABC, abstractmethod


class DAO(ABC):

    @abstractmethod
    def create_connection(self, **kwargs):
        pass

    @abstractmethod
    def read_data(self, **kwargs):
        pass

    @abstractmethod
    def insert_data(self, **kwargs):
        pass

    @abstractmethod
    def update_data(self, **kwargs):
        pass

    @abstractmethod
    def delete_data(self, **kwargs):
        pass

    @abstractmethod
    def close_connection(self):
        pass

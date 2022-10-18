from abc import ABC, abstractmethod


class DAO(ABC):

    @abstractmethod
    def create_connection(self, **kwargs) -> None:
        pass

    @abstractmethod
    def read_data(self, **kwargs) -> None:
        pass

    @abstractmethod
    def insert_data(self, **kwargs) -> None:
        pass

    @abstractmethod
    def update_data(self, **kwargs) -> None:
        pass

    @abstractmethod
    def delete_data(self, **kwargs) -> None:
        pass

    @abstractmethod
    def close_connection(self) -> None:
        pass

    @abstractmethod
    def populate_database(self, data_folder: str):
        pass

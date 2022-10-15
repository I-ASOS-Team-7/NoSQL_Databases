import os
from typing import Optional

import pandas as pd


class Statistics:

    """Represents the Database Testing Statistics."""

    def __init__(
        self,
        export_folder_path: Optional[str] = os.path.join(
            os.getcwd(), 'data', 'output'
        )
    ) -> None:
        """Initializes the Statistics Class.

        Args:
            export_folder_path (Optional[str]): Database Testing Statistics 
            result export folder path. Defaults to os.path.join(os.getcwd(), 
            'data', 'output').
        """
        self.__export_folder_path: str = export_folder_path
        self.__insert_data: pd.DataFrame = None
        self.__update_data: pd.DataFrame = None
        self.__delete_data: pd.DataFrame = None

    def add_insert_time(
        self,
        database_type: str,
        database: str,
        dataset: str,
        time: float
    ) -> None:
        """Adds new Insert Time value to DataFrame.

        Args:
            database_type (str): Type of NoSQL Database.
            database (str): Name of the NoSQL Database.
            dataset (str): Name of the Dataset/Collection in NoSQL Database.
            time (float): Execution Time.
        """
        data = {
            'database_type': database_type,
            'database': database,
            'dataset': dataset,
            'time': time
        }

        if self.__insert_data is None:
            self.__insert_data = pd.DataFrame(
                data,
                index=[0]
            )
        else:
            self.__insert_data = pd.concat(
                [
                    self.__insert_data,
                    pd.DataFrame(
                        data,
                        index=[0]
                    )
                ],
                axis=0,
                ignore_index=True
            )

    def add_update_time(
        self,
        database_type: str,
        database: str,
        dataset: str,
        time: float
    ) -> None:
        """Adds new Update Time value to DataFrame.

        Args:
            database_type (str): Type of NoSQL Database.
            database (str): Name of the NoSQL Database.
            dataset (str): Name of the Dataset/Collection in NoSQL Database.
            time (float): Execution Time.
        """
        data = {
            'database_type': database_type,
            'database': database,
            'dataset': dataset,
            'time': time
        }

        if self.__update_data is None:
            self.__update_data = pd.DataFrame(
                data,
                index=[0]
            )
        else:
            self.__update_data = pd.concat(
                [
                    self.__update_data,
                    pd.DataFrame(
                        data,
                        index=[0]
                    )
                ],
                axis=0,
                ignore_index=True
            )

    def add_delete_time(
        self,
        database_type: str,
        database: str,
        dataset: str,
        time: float
    ) -> None:
        """Adds new Delete Time value to DataFrame.

        Args:
            database_type (str): Type of NoSQL Database.
            database (str): Name of the NoSQL Database.
            dataset (str): Name of the Dataset/Collection in NoSQL Database.
            time (float): Execution Time.
        """
        data = {
            'database_type': database_type,
            'database': database,
            'dataset': dataset,
            'time': time
        }

        if self.__delete_data is None:
            self.__delete_data = pd.DataFrame(
                data,
                index=[0]
            )
        else:
            self.__delete_data = pd.concat(
                [
                    self.__delete_data,
                    pd.DataFrame(
                        data,
                        index=[0]
                    )
                ],
                axis=0,
                ignore_index=True
            )

    def export_data_to_csv(self) -> None:
        """Exports each Time DataFrame to separate CSV File."""
        datasets = [self.__insert_data, self.__update_data, self.__delete_data]
        filenames = [
            'NoSQL_Databases_Insert_Times',
            'NoSQL_Databases_Update_Times',
            'NoSQL_Databases_Delete_Times'
        ]

        for dataset, filename in zip(datasets, filenames):
            if dataset is not None:
                dataset.to_csv(
                    os.path.join(
                        self.__export_folder_path,
                        f'{filename}.csv'
                    ),
                    index=False
                )

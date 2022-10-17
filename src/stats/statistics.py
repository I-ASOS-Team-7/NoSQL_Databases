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
		self.__execution_times: pd.DataFrame = None

	def add_execution_time(
		self,
		database_type: str,
		database: str,
		dataset: str,
		action: str,
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
			'action': action,
			'time': time
		}

		if self.__execution_times is None:
			self.__execution_times = pd.DataFrame(
				data,
				index=[0]
			)
		else:
			self.__execution_times = pd.concat(
				[
					self.__execution_times,
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
		if self.__execution_times is not None:
			self.__execution_times.to_csv(
				os.path.join(
					self.__export_folder_path,
					f'NoSQL_Databases_Execution_Times.csv'
				),
				index=False
			)

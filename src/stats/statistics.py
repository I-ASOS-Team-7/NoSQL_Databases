import os
from typing import Optional

import pandas as pd
import plotly.express as px


class Statistics:

	"""Represents the Database Testing Statistics."""

	def __init__(
		self,
		iterations: int,
		export_folder_path: Optional[str] = os.path.join(
			os.getcwd(), 'data', 'output'
		)
	) -> None:
		"""Initializes the Statistics Class.

		Args:
			iterations (int): Number of iterations.
			export_folder_path (Optional[str]): Database Testing Statistics 
			result export folder path. Defaults to os.path.join(os.getcwd(), 
			'data', 'output').
		"""
		self.__iterations: int = iterations 
		self.__export_folder_path: str = export_folder_path
		self.__execution_times: pd.DataFrame = None

		if not os.path.exists(self.__export_folder_path):
			os.mkdir(self.__export_folder_path)

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

	def __display_statistics(
		self, 
		database_type: str, 
		dataset: str, 
		action: str
	) -> None:
		print(
			self.__execution_times[
				(self.__execution_times['database_type'] == database_type) &
				(self.__execution_times['dataset'] == dataset) &
				(self.__execution_times['action'] == action)
			].describe().transpose(),
			end='\n\n'
		)

	def display_statistics(self) -> None:
		"""Displays basic statistics and distribution of execution times."""
		for database_type in sorted(
			list(self.__execution_times['database_type'].unique())
		):
			for dataset in sorted(
				list(self.__execution_times['dataset'].unique())
			):
				for action in sorted(
					list(self.__execution_times['action'].unique())
				):
					print(f"{database_type} {dataset.split('.')[0]} {action}")
					self.__display_statistics(
						database_type=database_type,
						dataset=dataset.split('.')[0],
						action=action
					)

	def __export_plot(self, action:str) -> None:
		selected_data = (
			self.__execution_times[self.__execution_times['action'] == action]
				.groupby(['database_type', 'dataset']).mean()
		).reset_index().sort_values(['dataset', 'time'], ascending=False)

		fig = px.bar(
			selected_data, 
			x='time', 
			y='dataset', 
			color='database_type', 
			orientation='h', 
			log_x=True, 
			barmode='group',
		)

		fig.update_layout(
			title=(
				f'NoSQL Databases - {action.capitalize()}' 
				f'({self.__iterations} Iterations)'
			),
			xaxis_title='Avg. Time (sec)',
			yaxis_title='Dataset',
			legend_title='Database Type',
			font=dict(
				size=18,
			), 
			title_x=0.5
		)

		filename = f'NoSQL_Databases_-_{action.capitalize()}'
		html_export_path = os.path.join(
			self.__export_folder_path, 'plots', 'html'
		)

		if not os.path.exists(html_export_path):
			os.mkdir(html_export_path)

		fig.write_html(
			os.path.join(
				html_export_path,f'{filename}_{self.__iterations}.html'
			)
		)

		fig.show()

	def export_plots(self) -> None:
		"""Exports every Execution Time Plot for each action."""
		for action in sorted(list(self.__execution_times['action'].unique())):
			self.__export_plot(action=action)

	def export_data_to_csv(self) -> None:
		"""Exports each Time DataFrame to separate CSV File."""
		if self.__execution_times is not None:
			self.__execution_times.to_csv(
				os.path.join(
					self.__export_folder_path,
					f'NoSQL_Databases_Execution_Times_{self.__iterations}.csv'
				),
				index=False
			)

	def __call__(self) -> None:
		"""Makes the Statistics Class callable and triggers all exports."""
		self.export_plots()
		self.display_statistics()
		self.export_data_to_csv()
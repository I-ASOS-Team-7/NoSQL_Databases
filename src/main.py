from dotenv import load_dotenv

from stats.statistics import Statistics
from utils import (
	run_couchdb,
	run_mongodb
)


if __name__ == '__main__':
	load_dotenv()

	statistics = Statistics()

	iterations = 1

	run_mongodb(statistics, iterations)
	run_couchdb(statistics, iterations)

	statistics.export_data_to_csv()

	

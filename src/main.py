import statistics
from dotenv import load_dotenv
from stats.statistics import Statistics

from utils import (
	run_couchdb,
	run_mongodb
)


if __name__ == '__main__':
	load_dotenv()

	statistics = Statistics()

	run_mongodb(statistics)
	# run_couchdb(statistics)

	statistics.export_data_to_csv()

	

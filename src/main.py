from dotenv import load_dotenv

from stats.statistics import Statistics
from utils import (
	run_couchdb,
	run_mongodb,
	run_neo4j,
	run_redis
)


if __name__ == '__main__':
	load_dotenv()
	iterations = 50

	statistics = Statistics(iterations)

	run_couchdb(statistics, iterations)
	run_neo4j()
	run_mongodb(statistics, iterations)
	run_redis(statistics, iterations)

	statistics()

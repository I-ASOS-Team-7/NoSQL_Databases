import statistics
from dotenv import load_dotenv
from stats.statistics import Statistics

from utils import run_mongodb


if __name__ == '__main__':
    load_dotenv()

    statistics = Statistics()

    run_mongodb(statistics)

    

from dotenv import load_dotenv

from utils import run_mongodb


if __name__ == '__main__':
    load_dotenv()

    run_mongodb()

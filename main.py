from environs import Env
from src.data.db import init_db
from src.cli.app import run_cli


def main():
    env = Env()
    env.read_env()

    db_path = env.str("DB_PATH")
    init_db(db_path)

    run_cli(db_path)


if __name__ == "__main__":
    main()

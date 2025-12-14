from environs import Env
from src.data.db import init_db


def main():
    env = Env()
    env.read_env()

    db_path = env.str("DB_PATH")
    print(f"Database path: {db_path}")
    
    init_db(db_path)
    print("Database geinstalleerd en geinitialiseerd")

if __name__ == "__main__":
    main()

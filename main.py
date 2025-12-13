from environs import Env

def main():
    env = Env()
    env.read_env()

    db_path = env.str("DB_PATH")
    print(f"Database path: {db_path}")

if __name__ == "__main__":
    main()

from postgresUtils.postgresUtils import PostgresDbUtils

def main():
    db = PostgresDbUtils()
    db.execute_query("SELECT * FROM users")
    print(db.execute_query("SELECT * FROM users"))

if __name__ == "__main__":
    main()
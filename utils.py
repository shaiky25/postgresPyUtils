import os
import psycopg2
from psycopg2 import pool
from configparser import ConfigParser

def get_db_connection():
    """
    Create a connection to the PostgreSQL database using credentials from properties file
    Returns:
        connection: PostgreSQL database connection
    """
    try:
        # Read database configuration from properties file
        config = ConfigParser()
        config.read('db_config.properties')
        
        # Get database connection parameters
        db_params = {
            'host': config.get('postgresql', 'host'),
            'database': config.get('postgresql', 'database'),
            'user': config.get('postgresql', 'user'),
            'password': config.get('postgresql', 'password'),
            'port': config.get('postgresql', 'port')
        }
        
        # Create connection pool
        connection_pool = pool.SimpleConnectionPool(
            1,  # minconn
            10, # maxconn
            **db_params
        )
        
        # Get connection from pool
        connection = connection_pool.getconn()
        
        return connection
        
    except Exception as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        raise

def close_db_connection(connection):
    """
    Close the database connection and return it to the pool
    Args:
        connection: PostgreSQL database connection
    """
    if connection:
        connection.close()

# Example usage:
# db = DatabaseConnection()
# 
# # Simple query
# results = db.execute_query("SELECT * FROM users WHERE id = %s", (1,))
# 
# # Transaction
# queries = [
#     ("INSERT INTO users (name) VALUES (%s)", ("John",)),
#     ("UPDATE users SET status = %s WHERE name = %s", ("active", "John"))
# ]
# db.execute_transaction(queries)

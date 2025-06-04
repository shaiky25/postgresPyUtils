
import os
import psycopg2
from psycopg2 import pool
from configparser import ConfigParser
class PostgresDbUtils:
    def __init__(self):
        self.connection_pool = None
        self._initialize_pool()

    def _initialize_pool(self):
        """Initialize the connection pool with database parameters"""
        try:
            config = ConfigParser()
            config.read('db_config.properties')
            
            db_params = {
                'host': config.get('postgresql', 'host'),
                'database': config.get('postgresql', 'database'),
                'user': config.get('postgresql', 'user'),
                'password': config.get('postgresql', 'password'),
                'port': config.get('postgresql', 'port')
            }
            
            self.connection_pool = pool.SimpleConnectionPool(
                1,  # minconn
                10, # maxconn
                **db_params
            )
        except Exception as e:
            print(f"Error initializing connection pool: {e}")
            raise

    def get_connection(self):
        """
        Get a connection from the pool
        Returns:
            connection: PostgreSQL database connection
        """
        try:
            return self.connection_pool.getconn()
        except Exception as e:
            print(f"Error getting connection from pool: {e}")
            raise

    def release_connection(self, connection):
        """
        Release a connection back to the pool
        Args:
            connection: PostgreSQL database connection
        """
        if connection:
            self.connection_pool.putconn(connection)

    def execute_query(self, query, params=None):
        """
        Execute a query and return results
        Args:
            query (str): SQL query to execute
            params (tuple): Query parameters
        Returns:
            list: Query results
        """
        connection = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error executing query: {e}")
            raise
        finally:
            if connection:
                self.release_connection(connection)

    def execute_transaction(self, queries):
        """
        Execute multiple queries in a transaction
        Args:
            queries (list): List of (query, params) tuples
        """
        connection = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            for query, params in queries:
                cursor.execute(query, params or ())
            
            connection.commit()
            cursor.close()
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error executing transaction: {e}")
            raise
        finally:
            if connection:
                self.release_connection(connection)

    def __del__(self):
        """Cleanup connection pool on object destruction"""
        if self.connection_pool:
            self.connection_pool.closeall()





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
        print(db_params.host,' ',db_params.database,' ',db_params.user,' ',db_params.password,' ',db_params.port)
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

# # Example usage:
# db = DatabaseConnection()
# # 
# # # Simple query
# results = db.execute_query("SELECT * FROM users WHERE id = %s", (1,))
# # 
# # # Transaction
# queries = [
#     ("INSERT INTO users (name) VALUES (%s)", ("John",)),
#     ("UPDATE users SET status = %s WHERE name = %s", ("active", "John"))
# ]
# db.execute_transaction(queries)
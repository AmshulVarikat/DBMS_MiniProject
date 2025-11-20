import mysql.connector
from mysql.connector import Error, pooling
import getpass

# Global connection pool
connection_pool = None
db_config = None

def initialize_connection_pool():
    """Initialize the connection pool once at startup"""
    global connection_pool, db_config
    
    if connection_pool is not None:
        return True
    
    try:
        password = getpass.getpass("Enter MySQL password for root: ")
        
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": password,
            "database": "vehicle_workshop_management"
        }
        
        # Create connection pool with 5-10 connections
        connection_pool = pooling.MySQLConnectionPool(
            pool_name="workshop_pool",
            pool_size=5,
            pool_reset_session=True,
            **db_config
        )
        
        print("✓ Connected to MySQL database!")
        print("✓ Connection pool initialized")
        return True
        
    except Error as e:
        print(f"✗ Error while connecting to MySQL: {e}")
        return False

def get_connection():
    """Get a connection from the pool"""
    global connection_pool
    
    if connection_pool is None:
        if not initialize_connection_pool():
            return None
    
    try:
        return connection_pool.get_connection()
    except Error as e:
        print(f"Error getting connection from pool: {e}")
        return None

def run_query(query, params=None, fetch=False):
    """
    Generic query runner with connection pooling
    
    Args:
        query: SQL query string
        params: Query parameters (tuple or None)
        fetch: If True, returns result set; if False, commits transaction
    
    Returns:
        - List of dict rows if fetch=True and successful
        - True if fetch=False and successful
        - Error string if failed
        - None if connection failed
    """
    conn = get_connection()
    if not conn:
        return "Failed to connect to database"

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
            return True
            
    except Error as e:
        # Rollback on error
        if conn:
            conn.rollback()
        print(f"Query Error: {e}")
        return str(e)
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def test_connection():
    """Test database connection and return status"""
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            return True, "Connection successful"
        return False, "Failed to get connection"
    except Error as e:
        return False, str(e)

def close_pool():
    """Close all connections in the pool (call on app exit)"""
    global connection_pool
    if connection_pool:
        try:
            # Connection pools don't have a direct close method
            # Connections are closed when they're returned to the pool
            connection_pool = None
            print("Connection pool closed")
        except Exception as e:
            print(f"Error closing pool: {e}")
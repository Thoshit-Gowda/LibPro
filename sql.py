import mysql.connector as m
from mysql.connector import Error

conn = m.connect(
    host="localhost",
    user="root",
    passwd="12345",
    db="LibPro"
)
cursor = conn.cursor()

def fAll(query, params=None):
    try:
        cursor.execute(query, params or ())
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching all data: {e}")
        return None
    finally:
        cursor.close()

def fOne(query, params=None):
    try:
        cursor.execute(query, params or ())
        return cursor.fetchone()
    except Error as e:
        print(f"Error fetching one row: {e}")
        return None
    finally:
        cursor.close()

def fMany(query, size, params=None):
    try:
        cursor.execute(query, params or ())
        return cursor.fetchmany(size)
    except Error as e:
        print(f"Error fetching many rows: {e}")
        return None
    finally:
        cursor.close()

def execQy(query, params=None):
    try:
        cursor.execute(query, params or ())
        conn.commit()
        print("Query executed successfully.")
    except Error as e:
        print(f"Error executing query: {e}")
        conn.rollback()
    finally:
        cursor.close()

def closeCon():
    try:
        conn.close()
        print("Connection closed successfully.")
    except Error as e:
        print(f"Error closing connection: {e}")

closeCon()

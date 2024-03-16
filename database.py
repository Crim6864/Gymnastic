import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to database successfully")
        except mysql.connector.Error as err:
            print("Error:", err)

    def execute_query(self, query):
        if not self.connection:
            print("Database is not connected")
            return None
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print("Error executing query:", err)
            return None
        finally:
            cursor.close()

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed")

# Database connection information
db_info = {
    'host': "rdbms.strato.de",
    'user': "dbu3805768",
    'password': "SQcWLEg5BAR5qVv",
    'database': "dbs12691858"
}

# Example usage:
# db = Database(**db_info)
# db.connect()
# result = db.execute_query("SELECT * FROM your_table;")
# print(result)
# db.close_connection()

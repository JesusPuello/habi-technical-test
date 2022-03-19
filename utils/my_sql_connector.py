import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseHandler:
    def __init__(self) -> None:
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("HOST"),
                database=os.getenv("DATABASE"),
                port=os.getenv("PORT"),
                user=os.getenv("USER"),
                password=os.getenv("PASSWORD"),
            )
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                self.cursor = self.connection.cursor()
                self.cursor.execute("select database();")
                record = self.cursor.fetchone()
                print("You're connected to database: ", record)
        except Error as e:
            print("Error while connecting to MySQL", e)
            self.close_all()

    def close_all(self) -> None:
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")

import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "traffic.db"



class UserDatabase:


    def __init__(self):

        self.conn = sqlite3.connect(
            DATABASE_PATH
        )

        self.cursor = self.conn.cursor()

        self.create_table()



    def create_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE,

            password TEXT,

            created_at TEXT

        )

        """)

        self.conn.commit()



    def add_user(
            self,
            username,
            password
    ):


        password = hashlib.sha256(
            password.encode()
        ).hexdigest()


        try:

            self.cursor.execute("""

            INSERT INTO users
            (
            username,
            password,
            created_at
            )

            VALUES(?,?,?)

            """,

            (
            username,
            password,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            ))


            self.conn.commit()

            return True


        except sqlite3.IntegrityError:

            return False



    def verify_user(
            self,
            username,
            password
    ):


        password = hashlib.sha256(
            password.encode()
        ).hexdigest()


        self.cursor.execute("""

        SELECT *

        FROM users

        WHERE username=?

        AND password=?

        """,

        (
        username,
        password
        ))


        user = self.cursor.fetchone()


        return user is not None



    def close(self):

        self.conn.close()
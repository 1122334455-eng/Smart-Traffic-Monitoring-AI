"""
=========================================
Smart Traffic Monitoring System

Database Module

Author : Sharif Ullah
=========================================
"""


import sqlite3
from datetime import datetime
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "traffic.db"





class TrafficDatabase:



    def __init__(self):

        self.conn = sqlite3.connect(

            DATABASE_PATH,

            timeout=30,

            check_same_thread=False

        )


        self.cursor = self.conn.cursor()


        self.create_table()






    def create_table(self):


        self.cursor.execute(

        """

        CREATE TABLE IF NOT EXISTS traffic_logs(


            id INTEGER PRIMARY KEY AUTOINCREMENT,


            session_id INTEGER,


            vehicle_id INTEGER,


            vehicle TEXT,


            speed REAL,


            violation TEXT,


            density TEXT,


            entry INTEGER DEFAULT 0,


            exit INTEGER DEFAULT 0,


            timestamp TEXT


        )


        """

        )


        self.conn.commit()






    # ===============================
    # Insert New Vehicle
    # ===============================


    def insert_data(

            self,

            session_id,

            vehicle_id,

            vehicle,

            speed,

            violation,

            density,

            entry,

            exit

    ):



        self.cursor.execute(

        """

        INSERT INTO traffic_logs


        (

        session_id,

        vehicle_id,

        vehicle,

        speed,

        violation,

        density,

        entry,

        exit,

        timestamp

        )


        VALUES(?,?,?,?,?,?,?,?,?)


        """,


        (

        session_id,

        vehicle_id,

        vehicle,

        speed,

        violation,

        density,

        entry,

        exit,

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        )


        )


        self.conn.commit()








    # ===============================
    # Update Existing Vehicle
    # ===============================


    def update_vehicle(

            self,

            session_id,

            vehicle_id,

            speed,

            violation,

            density,

            entry,

            exit

    ):



        self.cursor.execute(

        """

        UPDATE traffic_logs


        SET


        speed=?,

        violation=?,

        density=?,


        entry = entry + ?,


        exit = exit + ?,


        timestamp = ?



        WHERE session_id=?

        AND vehicle_id=?



        """,



        (

        speed,

        violation,

        density,

        entry,

        exit,

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),


        session_id,

        vehicle_id


        )

        )



        self.conn.commit()








    # ===============================
    # Fetch Dashboard Data
    # ===============================


    def fetch_all(self):


        self.cursor.execute(

        """

        SELECT


        id,

        session_id,

        vehicle_id,

        vehicle,

        speed,

        violation,

        density,

        entry,

        exit,

        timestamp



        FROM traffic_logs



        ORDER BY id DESC



        """

        )



        return self.cursor.fetchall()








    # ===============================
    # Latest Session
    # ===============================


    def get_latest_session(self):


        self.cursor.execute(

        """

        SELECT MAX(session_id)

        FROM traffic_logs


        """

        )


        result = self.cursor.fetchone()


        return result[0] if result[0] else None








    # ===============================
    # Close Database
    # ===============================


    def close(self):


        self.conn.close()
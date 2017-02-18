"""
Author: Kevin Flathers
Date Created: 02/09/2017
Date Last Edited: 02/13/2017
Course: CS521

The requirements for exactly what this file must do can be seen
in the attached file, CS521_Project_Part2.docx. Further explanation
as to what each class does is given within the respective class.
"""

import sqlite3
import collections


class AbstractDAO:
    """
    Generic DAO class to be inherited
    """
    db_name = ""

    def insert_records(self, records):
        raise NotImplementedError

    def select_all(self):
        raise NotImplementedError

    def connect(self):
        return sqlite3.connect(self.db_name)


class BaseballStatsDAO(AbstractDAO):
    """
    DAO for baseball statistics
    """

    def insert_records(self, records):
        current_db = self.connect()
        cursor = current_db.cursor()
        for record in records:
            cursor.execute("""
                INSERT INTO ? (player_name, game_played, average, salary)
                VALUES(?, ?, ?, ?)
            """, (record['PLAYER'], record['G'], record['AVG'], record['SALARY']))
        current_db.commit()
        current_db.close()

    def select_all(self):
        current_db = self.connect()
        cursor = current_db.cursor()
        records = collections.deque()
        cursor.execute("""
            SELECT * FROM baseball_stats
        """)
        for record in cursor:
            records.append(BaseballStatRecord(record))
        current_db.close()
        return records

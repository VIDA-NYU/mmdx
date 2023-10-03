import threading
import sqlite3
from typing import NamedTuple


class DBConn(NamedTuple):
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

db_conns: dict[str:DBConn] = {}

def get_db_connection(db_file: str) -> DBConn:
    # Get or create a thread-local variable for the given database file,
    # and use it to store SQLite db connections
    thread_local_db = db_conns.get(db_file, threading.local())
    # Check if the current thread already has a connection. If not,
    # create a new connection and set it as a thread-local variable
    if not hasattr(thread_local_db, "connection"):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        thread_local_db.connection = DBConn(conn, cursor)
    return thread_local_db.connection


class LabelsDB:
    def __init__(self, db_file: str):
        self.db_file = db_file
        _, cursor = get_db_connection(db_file)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS labels (
                image_path TEXT,
                label TEXT
            );
        """
        )

    def add(self, image_path: str, label: str):
        conn, cursor = get_db_connection(self.db_file)
        cursor.execute(
            "INSERT INTO labels (image_path, label) VALUES (?, ?);",
            (image_path, label),
        )
        conn.commit()

    def remove(self, image_path: str, label: str):
        conn, cursor = get_db_connection(self.db_file)
        cursor.execute(
            "DELETE FROM labels WHERE image_path=? AND label=?;",
            (image_path, label),
        )
        conn.commit()

    def get(self, image_path: str = None) -> list[str]:
        _, cursor = get_db_connection(self.db_file)
        if image_path is None:
            cursor.execute("SELECT DISTINCT label FROM labels;")
        else:
            cursor.execute(
                "SELECT DISTINCT label FROM labels WHERE image_path=?;",
                (image_path,),
            )
        return [row[0] for row in cursor.fetchall()]

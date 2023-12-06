import threading
import sqlite3
from typing import NamedTuple, List, Dict, Optional


class DBConn(NamedTuple):
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor


db_conns: Dict[str, threading.local] = {}


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
        self.tables = ["animal", "relevant", "labels", "description", "keywords"]
        self.create_tables(cursor)


    def create_tables(self, cursor):
        for table in self.tables:
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    image_path TEXT,
                    label TEXT
                );
            """
            )

    def add(self, image_path: str, label: str, table: str):
        conn, cursor = get_db_connection(self.db_file)
        cursor.execute(
            f"INSERT INTO {table} (image_path, label) VALUES (?, ?);",
            (image_path, label),
        )
        conn.commit()

    def remove_records(self, **kwargs):
        table = kwargs.pop("table")
        conn, cursor = get_db_connection(self.db_file)
        # Generate the WHERE clause based on the provided parameters
        where_conditions = " AND ".join([f"{key}=?" for key in kwargs.keys()])
        values = tuple(kwargs.values())

        # Execute the DELETE statement
        cursor.execute(f"DELETE FROM {table} WHERE {where_conditions};", values)

        conn.commit()

    def get(self,  table: str, image_path: Optional[str] = None) -> List[str]:
        _, cursor = get_db_connection(self.db_file)
        if image_path is None:
            query = f"SELECT DISTINCT relevant.label FROM relevant"
            # for table_name in ["animal, description"]:
            #     query += f" LEFT JOIN {table_name} ON relevant.label = {table_name}.label"
            cursor.execute(query)
        else:
            query = f"SELECT DISTINCT relevant.label FROM labels"
            for table_name in ["animal, description"]:
                query += f" LEFT JOIN {table_name} ON relevant.label = {table_name}.label WHERE {table_name}.image_path = ?"
            cursor.execute(query + ";", (image_path,))
        return [row[0] for row in cursor.fetchall()]

    def counts(self) -> dict[str, int]:
        _, cursor = get_db_connection(self.db_file)
        cursor.execute("SELECT label, COUNT(*) FROM labels GROUP BY label;")
        counts = {}
        for row in cursor.fetchall():
            counts[row[0]] = row[1]
        return counts

    def get_image_paths(self) -> List[str]:
        _, cursor = get_db_connection(self.db_file)
        cursor.execute("SELECT DISTINCT image_path FROM labels;")
        return [row[0] for row in cursor.fetchall()]

    def create_zip_labeled_data(
            self,
            output_dir: str,
            filename: str) -> str:
        _, cursor = get_db_connection(self.db_file)
        query = """
        SELECT
            COALESCE(animal.image_path, description.image_path, relevant.image_path) AS image_path,
            animal.label AS animal,
            GROUP_CONCAT(description.label, ', ') AS description,
            relevant.label AS relevant
        FROM
            animal
        LEFT JOIN
            description ON animal.image_path = description.image_path
        LEFT JOIN
            relevant ON animal.image_path = relevant.image_path
        GROUP BY
            COALESCE(animal.image_path, description.image_path, relevant.image_path), animal.label, relevant.label;

        """
        cursor.execute(query)
        result = cursor.fetchall()
        return result

from pathlib import Path
import sqlite3


class DB:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def __enter__(self):
        self.connection: sqlite3.Connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor: sqlite3.Cursor = self.connection.cursor()
        return self

    def __exit__(self, exec_type, exec_value, exec_traceback):
        self.connection.close()

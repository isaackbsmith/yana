from pathlib import Path
import sqlite3

from yana.data.database import DB

def execute_migration(db_path: Path, sql: str, s: bool = False):
    with DB(db_path, sqlite3.Row) as db:
        cur = db.cursor.execute(sql)
        cur.connection.commit()
        if s:
           return cur.fetchall() 
        print("Finished executing sql")

def create_user():
    sql = """
        INSERT INTO users (
            id,
            first_name,
            last_name,
            email,
            phone_number,
            password,
            gender,
            user_type
        ) VALUES (
            'first',
            'john',
            'doe',
            'john@doe.com',
            '0000000000',
            'password',
            'male',
            'primary');
        """
    sql1 = "SELECT first_name FROM users WHERE id = 'a'"
    h = execute_migration("dev.db", sql, False)
    print(h)


if __name__ == "__main__":
    create_user()

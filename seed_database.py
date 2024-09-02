import sqlite3
from pathlib import Path
from typing import Any

from yana.data.database import DB
from yana.utils.data_loader import load_json


def run_query(db_path, sql, params: list[dict[str, Any]]) -> None:
    with DB(db_path, sqlite3.Row) as db:
        print("Executing query")
        db.cursor.executemany(sql, params)
        db.connection.commit()
        print("Finished executing query")


def seed_medication_routes(db_path: Path):
    sql = """
        INSERT INTO medication_routes (
            name,
            friendly_name,
            description
        )
        VALUES (
            :name,
            :friendly_name,
            :description
        );
        """

    path = Path("yana/static/medication_routes.json").resolve()
    params = load_json(path)

    try:
        run_query(db_path, sql, params)
    except Exception as e:
        print(f"An Error Occurred: {e}")


def seed_dosage_forms(db_path: Path):
    sql = """
        INSERT INTO dosage_forms (
            name,
            friendly_name,
            description
        )
        VALUES (
            :name,
            :friendly_name,
            :description
        );
        """

    path = Path("yana/static/dosage_forms.json").resolve()
    params = load_json(path)

    try:
        run_query(db_path, sql, params)
    except Exception as e:
        print(f"An Error Occurred: {e}")



def main() -> None:
    db_path = Path("dev.db").resolve()
    # seed_dosage_forms(db_path)
    seed_medication_routes(db_path)


if __name__ == "__main__":
    main()

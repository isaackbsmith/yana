import sys
import duckdb
from pathlib import Path
from collections.abc import Iterator


def fetch_migrations(directory: str) -> Iterator[Path]:
    """
    Fetch all migration files

    parameters:
        path: Path to the migration directory

    returns:
        A list of migration files
    """

    path = Path(directory)

    if not path.exists():
        print("Path does not exist")

    if path.is_file():
        raise Exception(f"{path} is not a folder")

    return path.glob("*.sql")


def migrate(db: str, schemas: list[Path]) -> None:
    """
    Execute all the schema files

    parameters:
        db: Path to the database
        schemas: A list of schema files

    returns:
        None
    """

    with duckdb.connect(db) as conn:
        for schema in schemas:
            print(f"Running Migration {schema}")
            conn.execute(schema.read_text())
        print("Finished running migrations")


def main() -> None:
    BASE_PATH = Path.cwd()

    db_path = sys.argv[1]

    # Fetch all files in the migrations folder
    migrations = list(fetch_migrations(f"{str(BASE_PATH)}/migrations"))

    # Sort them from oldest to newest
    sorted_migrations = sorted(migrations, key=lambda x: x.stat().st_mtime_ns)

    migrate(db_path, sorted_migrations)


if __name__ == "__main__":
    main()

import sys
from pathlib import Path
from collections.abc import Iterator

from yana.lib import DB


def fetch_migrations(path: Path) -> Iterator[Path]:
    """
    Fetch all migration files

    parameters:
        path: Path to the migration directory

    returns:
        A list of migration files
    """

    if not path.exists():
        print("Path does not exist")

    if path.is_file():
        raise Exception(f"{path} is not a folder")

    return path.glob("*.sql")


def sort_migrations(migrations: list[Path]) -> list[Path]:
    """
    Sorts the migrations from oldest to newest

    parameters:
        migrations: A list of schema files

    returns:
        None
    """
    return sorted(migrations, key=lambda x: x.stat().st_mtime_ns)


def migrate(db_path: Path, migrations: list[Path]) -> None:
    """
    Executes all the schema files

    parameters:
        db: Path to the database
        migrations: A list of schema files

    returns:
        None
    """

    with DB(db_path) as db:
        for schema in migrations:
            print(f"Running Migration {schema}")
            db.cursor.execute(schema.read_text())
        print("Finished running migrations")


def main() -> None:
    BASE_PATH = Path.cwd()

    try:
        db_path = Path(sys.argv[1]).resolve()

        # Fetch all files in the migrations folder
        migrations = list(fetch_migrations(BASE_PATH / "migrations"))

        # Sort them from oldest to newest and migrate
        sorted_migrations = sort_migrations(migrations)
        migrate(db_path, sorted_migrations)
    except IndexError:
        print("Database path missing")
        raise SystemExit()


if __name__ == "__main__":
    main()

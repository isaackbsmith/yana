import datetime
import tempfile
from pathlib import Path
from collections.abc import Iterator
import sqlite3

from yana.domain.db import DB


def fetch_schemas(path: Path) -> Iterator[Path]:
    """
    Fetch all schema files

    parameters:
        path: Path to the schema directory

    returns:
        A list of migration files
    """

    if not path.exists():
        print("Path does not exist")
        raise FileNotFoundError(f"{path} does not exist")

    if path.is_file():
        raise NotADirectoryError(f"{path} is not a directory")

    return path.glob("*.sql")


def sort_schemas(schemas: list[Path]) -> list[Path]:
    """
    Sorts the schemas from oldest to newest

    parameters:
        schemas: A list of schema files

    returns:
        None
    """
    return sorted(schemas, key=lambda x: x.stat().st_mtime_ns)


def create_migration(migration_file: Path, schemas: list[Path]) -> None:
    """
    Creates a new migration file by appending all the schemas

    parameters:
        migration_file: migration file
        schemas: A list of schema files

    returns:
        None
    """
    for schema in schemas:
        with migration_file.open(mode="a") as migration_f:
            migration_f.write(f"-- {schema.name}\n")
            migration_f.write(f"{schema.read_text().strip()}\n\n")


def execute_migration(db_path: Path, migration: Path) -> None:
    """
    Executes a migration file

    parameters:
        db: Path to the database
        migration: Migration schema file

    returns:
        None
    """
    with DB(db_path) as db:
        print(f"Validating migration: {migration}")
        db.cursor.executescript(migration.read_text())
        print("Finished validating migration")


def validate_migration(migration: Path) -> bool:
    """
    Runs the migration on a temporary database to verify
    the correctness of the migration.

    parameters:
        migrations: A migration file

    returns:
        True ? migration is valid : False
    """

    # create a tmp db
    with tempfile.NamedTemporaryFile(
        mode="w+", 
        suffix=".db",
        dir=".") as tmp_db:

        try:
            execute_migration(Path(tmp_db.name), migration)
            return True
        except sqlite3.OperationalError as e:
            print(f"migration Error {e}")
            return False
        except sqlite3.ProgrammingError as e:
            print(f"migration Error {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error {e}")
            return False


def main() -> None:
    BASE_PATH = Path.cwd()
    SCHEMA_DIR = BASE_PATH / "yana/data/models"
    MIGRATIONS_DIR = BASE_PATH / "migrations"

    try:
        # Fetch all files in the migrations folder
        schemas = list(fetch_schemas(SCHEMA_DIR))

        # Sort them from oldest to newest and migrate
        sorted_schemas = sort_schemas(schemas)

        print(sorted_schemas)

        # Create a new migration file
        migration_file = MIGRATIONS_DIR / f"{int(datetime.datetime.now().timestamp())}.sql"

        print(f"Creating migration file {migration_file}")
        create_migration(migration_file, sorted_schemas)

        if validate_migration(migration_file):
            print("Migration is valid")
        else:
            print("Migration is invalid...cleaning up")
            migration_file.unlink(missing_ok=True);
    except FileNotFoundError as e:
        print(f"Database does not exist: {e}")
        raise SystemExit()
    except NotADirectoryError as e:
        print(f"Database path is not a directory: {e}")
        raise SystemExit()


if __name__ == "__main__":
    main()

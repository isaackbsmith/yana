import tempfile
import argparse
from pathlib import Path
import sqlite3

from yana.domain.db import DB


def sort_migrations(migrations: list[Path]) -> list[Path]:
    """
    Sorts the migrations from oldest to newest

    parameters:
        migrations: A list of migration files

    returns:
        None
    """
    return sorted(migrations, key=lambda x: x.stem.split("_")[0])


def fetch_all_migrations(migrations_dir: Path) -> list[Path]:
    """
    Fetches all migrations and sorts them

    parameters:
        migrations_dir: The migrations directory

    returns:
        The sorted list of migrations
    """
    if not migrations_dir.exists():
        print("Path does not exist")
        raise FileNotFoundError(f"Path does not exist")

    if migrations_dir.is_file():
        raise NotADirectoryError(f"{migrations_dir} is not a directory")

    migration_files = list(migrations_dir.glob("*.sql"))
    sorted_migration_files = sort_migrations(migration_files)

    return sorted_migration_files


def fetch_applied_migrations(history: Path) -> set[str]:
    """
    Fetch migrations that have not been applied yet

    parameters:
        history: Path to the migration history

    returns:
        A set of applied migrations
    """
    applied_migrations = set()

    with history.open() as hist:
        for line in hist:
            applied_migrations.add(line.strip())

    return applied_migrations


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
        print(f"Executing migration: {migration}")
        db.cursor.executescript(migration.read_text())
        print("Finished executing migration")


def validate_migration(migrations_dir: Path) -> bool:
    """
    Runs the migration on a temporary database to verify
    the correctness of the migration.

    parameters:
        migrations: A migration file

    returns:
        True ? migration is valid : False
    """
    migration_files = fetch_all_migrations(migrations_dir)

    # create a tmp db
    with tempfile.NamedTemporaryFile(
        mode="w+", 
        suffix=".db",
        dir=".") as tmp_db:

        try:
            for migration_file in migration_files:
                print(f"Applying migration: {migration_file.stem}")
                execute_migration(Path(tmp_db.name), migration_file)
            print("Schema validated successfully")
            return True
        except sqlite3.OperationalError as e:
            print(f"Migration Error {e}")
            return False
        except sqlite3.ProgrammingError as e:
            print(f"Migration Error {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error {e}")
            return False


def apply_migration(db_path: Path, migration: Path, history: Path) -> None:
    """
    Applies a migration file

    parameters:
        db: Path to the database
        migration: Migration schema file

    returns:
        None
    """
    try:
        execute_migration(db_path, migration)
        with history.open(mode="a") as hist:
            hist.write(f"{migration.name}\n")
    except sqlite3.OperationalError as e:
        print(f"Migration Error {e}")
    except sqlite3.ProgrammingError as e:
        print(f"Migration Error {e}")
    except sqlite3.Error as e:
        print(f"Error {e}")


def run_migrations(db_path: Path, migrations_dir: Path, history: Path):
    """
    Validates and applies new migrations

    parameters:
        db_path: Path to the target datastore
        migrations_dir: Path to the migrations directory
        history: Path to the migrations history
    """
    if not history.exists():
        print("Migration history file does not exist...creating history file")
        history.touch()

    if not migrations_dir.exists():
        print("Path does not exist")
        raise FileNotFoundError(f"Path does not exist")

    if migrations_dir.is_file():
        raise NotADirectoryError(f"{migrations_dir} is not a directory")

    migration_files = list(migrations_dir.glob("*.sql"))
    sorted_migration_files = sort_migrations(migration_files)
    applied_migrations = fetch_applied_migrations(history)

    for migration_file in sorted_migration_files:
        if migration_file.name not in applied_migrations:
            print(f"Applying migration: {migration_file.stem}")
            if validate_migration(migrations_dir):
                apply_migration(db_path, migration_file, history)
            else:
                print("Could not validate migration")
        else:
            print(f"Skipping already applied migration: {migration_file.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validates and applies migrations")

    parser.add_argument("-v", "--validate", action="store_true", help="Validates unapplied migrations")
    parser.add_argument("-m", "--migrate", action="store_true", help="Apply migrations")
    parser.add_argument("-t", "--target", type=str, default="dev.db", help="Taget datastore")

    args = parser.parse_args()

    BASE_PATH = Path.cwd()
    MIGRATIONS_DIR = BASE_PATH / "yana/data/migrations"
    MIGRATIONS_HISTORY = BASE_PATH / "yana/data/migrations/.mighist"

    try:
        db_path = Path(args.target).resolve()

        if args.validate:
            validate_migration(MIGRATIONS_DIR)
        
        if args.migrate:
            run_migrations(db_path, MIGRATIONS_DIR, MIGRATIONS_HISTORY)

    except Exception as e:
        print(f"An error occured: {e}")
        raise SystemExit()


if __name__ == "__main__":
    main()

import datetime
import textwrap
import argparse
import sqlite3
import tempfile
from pathlib import Path

from yana.data.database import DB


def create_migration_file(args: argparse.Namespace, migration_file: Path) -> None:
    """
    Creates a new migration file by appending all the schemas

    parameters:
        migration_file: migration file
        schemas: A list of schema files

    returns:
        None
    """
    prefix = f"-- {args.name} Generated on {datetime.datetime.now()}\n\n"
    template = textwrap.dedent(
        f"""
                -- Entity table
                CREATE TABLE IF NOT EXISTS {args.name} (
                    id VARCHAR(36) PRIMARY KEY,
                    created_at INTEGER NOT NULL,
                    updated_at INTEGER NOT NULL
                ) WITHOUT ROWID;


                -- Triggers for automatic creation and updation timestamps (UNIX epoch)
                CREATE TRIGGER set_{args.name}_timestamps
                AFTER INSERT ON {args.name}
                BEGIN
                    UPDATE {args.name}
                    SET
                        created_at = strftime('%s', 'now'),
                        updated_at = strftime('%s', 'now')
                    WHERE id = NEW.id;
                END;

                CREATE TRIGGER update_{args.name}_timestamps
                AFTER INSERT ON {args.name}
                BEGIN
                    UPDATE {args.name}
                    SET updated_at = strftime('%s', 'now')
                    WHERE id = NEW.id;
                END;
            \n"""
    ).strip()

    if args.create:
        with migration_file.open(mode="a") as migration_f:
            migration_f.write(prefix)
            migration_f.write(template)
    else:
        with migration_file.open(mode="a") as migration_f:
            migration_f.write(prefix)


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
        raise FileNotFoundError(f"Path {migrations_dir} does not exist")

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
    with DB(db_path, sqlite3.Row) as db:
        print(f"Executing {migration}")
        db.cursor.executescript(migration.read_text())
        print(f"Finished executing {migration}")


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
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".db", dir=".") as tmp_db:
        db_path = Path(tmp_db.name)

        try:
            for migration_file in migration_files:
                execute_migration(db_path, migration_file)
            print("Schema is valid")
            return True
        except sqlite3.Error as e:
            print("Migration invalid")
            print(f"Database Error {e}")
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
    except sqlite3.Error as e:
        print(f"Database Error {e}")


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

    if not validate_migration(migrations_dir):
        print("Could not validate migration")
    else:
        for migration_file in sorted_migration_files:
            if migration_file.name not in applied_migrations:
                print(f"Applying migration: {migration_file.stem}")
                apply_migration(db_path, migration_file, history)
            else:
                print(f"Skipping already applied migration: {migration_file.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Creates new migration files")

    # Create subparsers for each command
    sub_parsers = parser.add_subparsers(dest="command", help="For sub-commands")

    # Make migrations
    makemigration_parser = sub_parsers.add_parser(
        "makemigration", help="Create a new migration file"
    )
    makemigration_parser.add_argument(
        "-c", "--create", action="store_true", help="Create Entity"
    )
    makemigration_parser.add_argument("-n", "--name", type=str, help="Migration name")

    # Mmigrate
    migrate_parser = sub_parsers.add_parser("migrate", help="Apply migrations")
    migrate_parser.add_argument(
        "-t", "--target", type=str, default="dev.db", help="Taget datastore"
    )

    # Validate migration
    validatemigration_parser = sub_parsers.add_parser(
        "validatemigration", help="Validate migration"
    )

    args = parser.parse_args()

    BASE_PATH = Path.cwd()
    MIGRATIONS_DIR = BASE_PATH / "yana/data/migrations"
    MIGRATIONS_HISTORY = BASE_PATH / "yana/data/migrations/.mighist"

    try:
        if args.command == "makemigration":
            if not args.name:
                print("Migration file name is missing")
                raise SystemExit()
            migration_file = (
                MIGRATIONS_DIR
                / f"{int(datetime.datetime.now().timestamp())}_{args.name}.sql"
            )
            print(f"Creating migration file {migration_file}")
            create_migration_file(args, migration_file)
        elif args.command == "migrate":
            db_path = Path(args.target).resolve()
            run_migrations(db_path, MIGRATIONS_DIR, MIGRATIONS_HISTORY)
        elif args.command == "validatemigration":
            validate_migration(MIGRATIONS_DIR)
        else:
            parser.print_help()
    except Exception as e:
        print(f"An Error Occurred: {e}")
        raise SystemExit()


if __name__ == "__main__":
    main()

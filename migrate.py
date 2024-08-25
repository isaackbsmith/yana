import sys
from pathlib import Path

from yana.domain.db import DB

def fetch_recent_migration(path: Path) -> Path | None:
    """
    Fetch the most recent migration

    parameters:
        path: Path to the migration

    returns:
        The most recent migration file
    """

    if not path.exists():
        print("Path does not exist")
        raise FileNotFoundError(f"{path} does not exist")

    if path.is_file():
        raise NotADirectoryError(f"{path} is not a directory")

    migrations = path.glob("*.sql")

    if migrations:
        recent_migration = sorted(migrations, key=lambda x: x.stem)[0]
        return recent_migration

    return None


def apply_migration(db_path: Path, migration: Path) -> None:
    """
    Executes a migration file

    parameters:
        db: Path to the database
        migration: Migration schema file

    returns:
        None
    """
    with DB(db_path) as db:
        print(f"Applying migration: {migration}")
        db.cursor.executescript(migration.read_text())
        print("Finished applying migration")


def main() -> None:
    BASE_PATH = Path.cwd()
    MIGRATIONS_DIR = BASE_PATH / "migrations"

    print(sys.argv)
    try:
        db_path = Path(sys.argv[1]).resolve()

        migration = fetch_recent_migration(MIGRATIONS_DIR)
        print(migration)

        if migration:
            apply_migration(db_path, migration)
        else:
            print("Migration directory is empty")
    except IndexError as e:
        print(f"Database path missing: {e}")
        raise SystemExit()
    except FileNotFoundError as e:
        print(f"Database does not exist: {e}")
        raise SystemExit()
    except NotADirectoryError as e:
        print(f"Database path is not a directory: {e}")
        raise SystemExit()


if __name__ == "__main__":
    main()

import sys
import pendulum
from pathlib import Path


def new_migration(filename: str) -> None:
    """
    Create a new migration file

    parameters:
        filename: Name of the new migration file

    returns:
        None
    """

    timestamp = pendulum.now()

    migration = Path(f"{filename}.sql")

    if not migration.parent.exists():
        print("Path does not exist")
        print("Creating Directory")
        migration.parent.mkdir(parents=True, exist_ok=True)

    if migration.exists():
        raise Exception(f"{migration} already exists")

    migration.write_text(
        f"-- Migration was created at {timestamp.to_datetime_string()}"
    )


def main() -> None:
    BASE_PATH = Path.cwd()
    MIGRATION_DIR = BASE_PATH / "migrations"

    filename = sys.argv[1]

    new_migration(str(MIGRATION_DIR / filename))


if __name__ == "__main__":
    main()

import datetime
import textwrap
import argparse
from pathlib import Path


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
            \n""").strip()

    if args.create:
        with migration_file.open(mode="a") as migration_f:
            migration_f.write(prefix)
            migration_f.write(template)
    else:
        with migration_file.open(mode="a") as migration_f:
            migration_f.write(prefix)


def main() -> None:
    parser = argparse.ArgumentParser(description="Creates new migration files")

    parser.add_argument("-c", "--create", action="store_true", help="Create Entity")
    parser.add_argument("-n", "--name", type=str, help="Migration name")

    args = parser.parse_args()

    BASE_PATH = Path.cwd()
    MIGRATIONS_DIR = BASE_PATH / "yana/data/migrations"

    try:
        # Create a new migration file
        if not args.name:
            print("Migration file name is missing")
            raise SystemExit()
        migration_file = MIGRATIONS_DIR / f"{int(datetime.datetime.now().timestamp())}_{args.name}.sql"
        print(f"Creating migration file {migration_file}")
        create_migration_file(args, migration_file)
    except Exception as e:
        print(f"An error occured: {e}")
        raise SystemExit()


if __name__ == "__main__":
    main()

import uuid
from _pytest import scope
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from manage import run_migrations
from seeder import seed_db
from yana.api.api import app
from yana.utils.config import get_config, get_test_config


config = get_test_config()
DB_PATH = Path(config.database.path)
MIGRATIONS_DIR = Path(config.database.migrations)
HISTORY_PATH = Path(config.database.history)

# Create database tables
run_migrations(DB_PATH, MIGRATIONS_DIR, HISTORY_PATH)

# Seed the database
seed_db(DB_PATH)


@pytest.fixture(scope="function", autouse=True)
def up_down():
    """Setup and teardown database and history file"""
    config = get_test_config()

    db_path = Path(config.database.path)
    migrations_dir = Path(config.database.migrations)
    history_path = Path(config.database.history)

    # Create database tables
    run_migrations(db_path, migrations_dir, history_path)

    # Seed the database
    seed_db(db_path)
    yield
    print("Tearing downn the up_down() fixture")
    Path(config.database.history).unlink()
    Path(config.database.path).unlink()


@pytest.fixture(scope="function")
def test_client():
    """Create a test client"""
    app.dependency_overrides[get_config] = get_test_config
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def new_id() -> str:
    """Generate a UUID string"""
    return str(uuid.uuid4())



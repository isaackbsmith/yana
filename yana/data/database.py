import sqlite3
from pathlib import Path
from pydantic import BaseModel
from typing import Any, Callable, Literal, TypeVar

from yana.domain.types import YANAConfig
from yana.domain.logger import root_logger
from yana.domain.exceptions import DatabaseError


T = TypeVar("T", bound=BaseModel)

RowFactory = Callable[[sqlite3.Cursor, tuple], T]


class DB:
    def __init__(self, db_path: Path, row_factory: RowFactory) -> None:
        self.db_path = db_path
        self.row_factory = row_factory

    def __enter__(self):
        self.connection: sqlite3.Connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = self.row_factory
        self.cursor: sqlite3.Cursor = self.connection.cursor()
        return self

    def __exit__(self, exec_type, exec_value, exec_traceback):
        self.connection.close()


def get_row_factory(factory: type[T]) -> RowFactory:
    def row_factory(cursor: sqlite3.Cursor, row: tuple) -> T:
        columns = [column[0] for column in cursor.description]
        # print("Factory: ======> ", dict(zip(columns, row)))
        return factory(**dict(zip(columns, row)))

    return row_factory


async def run_query(
    config: YANAConfig,
    sql: str,
    factory: type[T],
    params: dict[str, Any] | None = None,
    pragma: Literal["one", "all", "many"] | None = None,
    limit: int = 1,
) -> list[T] | T | None:
    db_path = Path(config.database.path).resolve()
    row_factory = get_row_factory(factory)

    with DB(db_path, row_factory) as db:
        try:
            if params:
                cursor = db.cursor.execute(sql, params)
            else:
                cursor = db.cursor.execute(sql)

            if pragma is None:
                db.connection.commit()
                return None

            if pragma == "one":
                return cursor.fetchone()
            elif pragma == "many":
                return cursor.fetchmany(limit)
            else:
                return cursor.fetchall()
        except sqlite3.Error as e:
            root_logger.error(f"Error executing query: {e}")
            raise DatabaseError(str(e))

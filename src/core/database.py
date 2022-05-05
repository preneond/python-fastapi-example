from typing import Any, List, Mapping, Optional, Sequence, Tuple, Union

import psycopg2
from psycopg2._psycopg import connection
from psycopg2.extras import RealDictCursor


class DatabaseConnection:
    """Database connection class"""

    conn: connection

    def __init__(
        self, conn: Optional[connection] = None, dsn: Optional[str] = None
    ) -> None:
        self.conn = conn or psycopg2.connect(dsn, cursor_factory=RealDictCursor)

    def query_all(
        self, query: str, params: Union[Sequence[Any], Mapping[str, Any], None] = None
    ) -> List[Tuple[Any, ...]]:
        """Execute a query and return the results"""
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def query_one(
        self, query: str, params: Union[Sequence[Any], Mapping[str, Any], None] = None
    ) -> Optional[Tuple[Any, ...]]:
        """Execute a query and return the results"""
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def execute(
        self, query: str, params: Union[Sequence[Any], Mapping[str, Any], None] = None
    ) -> None:
        """Execute a query and commit the changes"""
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
        self.conn.commit()  # type: ignore

    def close(self) -> None:
        """Close the connection"""
        self.conn.close()  # type: ignore

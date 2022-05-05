import asyncio
import json
import tempfile
from typing import Generator

import pytest
import pytest_asyncio
from psycopg2._psycopg import connection
from pydantic import EmailStr
from pytest_postgresql import factories
from starlette.responses import JSONResponse

from src.core.database import DatabaseConnection
from src.routers.user import (
    create_user_associated_value,
    delete_user_associated_value,
    get_users,
)
from src.schemas.requests import UserCreateRequest

socket_dir = tempfile.TemporaryDirectory()
postgresql_proc = factories.postgresql_proc(port=None, unixsocketdir=socket_dir.name)
postgresql_mocked = factories.postgresql(
    "postgresql_proc",
    load=["database/init.sql"],
)

EMAIL_LIST = [
    "leia@test.com",
    "obiwan@test.com",
    "chewbacca@test.com",
    "annakin@test.com",
    "darthvader@test.com",
    "jedi@test.com",
]


@pytest.fixture(scope="function")
def db_connection_mocked(
    postgresql_mocked: connection,
) -> Generator[DatabaseConnection, None, None]:
    db_connection = DatabaseConnection(conn=postgresql_mocked)
    yield db_connection
    db_connection.close()


@pytest_asyncio.fixture(scope="function")
async def mock_users(db_connection_mocked: DatabaseConnection) -> None:
    _ = await asyncio.gather(
        *[
            create_user_associated_value(
                user_in=UserCreateRequest(value="test_value"),
                email=EmailStr(email),
                db_connection=db_connection_mocked,
            )
            for email in EMAIL_LIST
        ]
    )


@pytest.mark.asyncio
async def test_query_empty_users(db_connection_mocked: DatabaseConnection) -> None:
    users_result: JSONResponse = await get_users(
        offset=0, limit=10, db_connection=db_connection_mocked
    )
    user_result_data = json.loads(users_result.body)["data"]
    assert len(user_result_data) == 0


@pytest.mark.asyncio
async def test_insert_users(
    db_connection_mocked: DatabaseConnection, n: int = 10
) -> None:
    """
    Test that the users are inserted correctly.
    The test is performed on :param n different users and the number of the users is verified
    :param db_connection_mocked: Database connection
    :param n: Number of users to insert
    :return: None
    """
    test_user_email_value_arr = [
        (f"user{i}@test.com", UserCreateRequest(value=f"value{i}")) for i in range(n)
    ]
    _ = await asyncio.gather(
        *[
            create_user_associated_value(
                user_in=test_user_in,
                email=EmailStr(test_user_email),
                db_connection=db_connection_mocked,
            )
            for test_user_email, test_user_in in test_user_email_value_arr
        ]
    )
    results = db_connection_mocked.query_all("SELECT * from users")
    assert len(results) == n


@pytest.mark.asyncio
async def test_update_user_value(db_connection_mocked: DatabaseConnection) -> None:
    """
    Test that the user value is updated correctly
    :param db_connection_mocked: Database connection
    :return: None
    """
    test_user_email = "user@test.com"
    test_user_in_value1 = UserCreateRequest(value="test_value")
    test_user_in_value2 = UserCreateRequest(value="test_value2")
    _ = await asyncio.gather(
        *[
            create_user_associated_value(
                user_in=test_user_in_value1,
                email=EmailStr(test_user_email),
                db_connection=db_connection_mocked,
            ),
            create_user_associated_value(
                user_in=test_user_in_value2,
                email=EmailStr(test_user_email),
                db_connection=db_connection_mocked,
            ),
        ]
    )
    results = db_connection_mocked.query_all("SELECT * from users")
    assert results[0][1] == "test_value2"


@pytest.mark.asyncio
async def test_delete_user(db_connection_mocked: DatabaseConnection) -> None:
    """
    Test that the user is deleted correctly
    :param db_connection_mocked: Database connection
    :param mock_users: Mocked users
    :return: None
    """
    test_user_email = "user@test.com"
    test_user_in_value1 = UserCreateRequest(value="test_value")
    _ = await asyncio.gather(
        *[
            create_user_associated_value(
                user_in=test_user_in_value1,
                email=EmailStr(test_user_email),
                db_connection=db_connection_mocked,
            ),
            delete_user_associated_value(
                email=EmailStr(test_user_email), db_connection=db_connection_mocked
            ),
        ]
    )

    results = db_connection_mocked.query_all("SELECT * from users")
    assert len(results) == 0


@pytest.mark.asyncio
async def test_users_alphabetical_sorting(
    db_connection_mocked: DatabaseConnection, mock_users: None
) -> None:
    """
    Test that the users are sorted alphabetically in [GET] /users
    :param db_connection_mocked: Database connection
    :param mock_users: Mocked users
    :return: None
    """
    users_result: JSONResponse = await get_users(
        offset=0, limit=10, db_connection=db_connection_mocked
    )
    user_result_data = json.loads(users_result.body)["data"]
    email_results = [result[0] for result in user_result_data]
    assert email_results == list(sorted(EMAIL_LIST))


@pytest.mark.asyncio
async def test_offset_users(
    db_connection_mocked: DatabaseConnection, mock_users: None
) -> None:
    """
    Test that the users are returned correctly with offset and limit
    :param db_connection_mocked: Database connection
    :param mock_users: Mocked users
    :return: None
    """
    users_result: JSONResponse = await get_users(
        offset=3, limit=10, db_connection=db_connection_mocked
    )
    user_result_data = json.loads(users_result.body)["data"]
    assert len(user_result_data) == 3

    users_result = await get_users(
        offset=10, limit=10, db_connection=db_connection_mocked
    )
    user_result_data = json.loads(users_result.body)["data"]
    assert len(user_result_data) == 0


@pytest.mark.asyncio
async def test_limit_users(
    db_connection_mocked: DatabaseConnection, mock_users: None
) -> None:
    """
    Test that the users are returned correctly with offset and limit
    :param db_connection_mocked: Database connection
    :param mock_users: Mocked users
    :return: None
    """
    users_result = await get_users(
        offset=0, limit=1, db_connection=db_connection_mocked
    )
    user_result_data = json.loads(users_result.body)["data"]
    assert len(user_result_data) == 1

    users_result = await get_users(
        offset=0, limit=100, db_connection=db_connection_mocked
    )
    user_result_data = json.loads(users_result.body)["data"]
    assert len(user_result_data) == 6

    users_result = await get_users(
        offset=0, limit=0, db_connection=db_connection_mocked
    )
    user_result_data = json.loads(users_result.body)["data"]
    assert len(user_result_data) == 0

    users_result = await get_users(
        offset=100, limit=0, db_connection=db_connection_mocked
    )
    user_result_data = json.loads(users_result.body)["data"]
    assert len(user_result_data) == 0

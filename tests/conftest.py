import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings
from app.db.models import Base
from app.db.postgres_session import get_session as get_db
from app.main import app
from app.schemas import word_schema
from app.services.word_crud import create_word


@pytest_asyncio.fixture(scope="function")
async def test_db_engine():
    engine = create_async_engine(settings.TEST_DATABASE_URL, echo=True, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_db_session(test_db_engine):
    async_session = async_sessionmaker(test_db_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(test_db_session):
    async def get_test_db():
        try:
            yield test_db_session
        finally:
            pass

    app.dependency_overrides[get_db] = get_test_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def inserted_word_by_id_in_test_db(test_db_session):
    await create_word(
        test_db_session, word_schema.WordCreate(word="журнал", translation="magazine", tg_user_id=1214104)
    )


@pytest_asyncio.fixture(scope="function")
async def word_test_data():
    return [
        {"word": "Книга", "translation": "Book", "tg_user_id": 121411},
        {"word": "Собака", "translation": "Dog", "tg_user_id": 121412},
        {"word": "Дом", "translation": "House", "tg_user_id": 121413},
        {"word": "Машина", "translation": "Car", "tg_user_id": 121414},
        {"word": "Река", "translation": "River", "tg_user_id": 121415},
        {"word": "Дерево", "translation": "Tree", "tg_user_id": 121416},
    ]


@pytest_asyncio.fixture(scope="function")
async def inserted_words_in_test_db(test_db_session, word_test_data):
    for data in word_test_data:
        await create_word(
            test_db_session,
            word_schema.WordCreate(
                word=data["word"], translation=data["translation"], tg_user_id=data["tg_user_id"]
            ),
        )


@pytest_asyncio.fixture(scope="function")
async def user_word_test_data():
    return [
        {"word": "Книга", "translation": "Book", "tg_user_id": 121411},
        {"word": "Собака", "translation": "Dog", "tg_user_id": 121412},
        {"word": "Интересный", "translation": "Integesting", "tg_user_id": 121411},
        {"word": "Дом", "translation": "House", "tg_user_id": 121411},
        {"word": "Зима", "translation": "Winter", "tg_user_id": 121411},
        {"word": "Удобный", "translation": "Convenient", "tg_user_id": 121411},
        {"word": "Интересный", "translation": "Integesting", "tg_user_id": 121444},
        {"word": "Дом", "translation": "House", "tg_user_id": 121444},
        {"word": "Зима", "translation": "Winter", "tg_user_id": 121444},
        {"word": "Удобный", "translation": "Winter", "tg_user_id": 121444},
    ]


@pytest_asyncio.fixture(scope="function")
async def inserted_user_specific_words(test_db_session, user_word_test_data):
    for data in user_word_test_data:
        await create_word(
            test_db_session,
            word_schema.WordCreate(
                word=data["word"], translation=data["translation"], tg_user_id=data["tg_user_id"]
            ),
        )

import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.settings import Settings
from app.infrastructure.database import Base


@pytest.fixture
def settings():
    return Settings()


@pytest_asyncio.fixture(scope="function")
def engine():
    engine = create_async_engine(url='postgresql+asyncpg://postgres:password@0.0.0.0:5433/pomodoro-test', future=True,
                                 echo=True, pool_pre_ping=True)
    return engine


@pytest_asyncio.fixture(autouse=True, scope="function")
async def init_models(event_loop, engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def get_db_session(event_loop, engine) -> AsyncSession:
    async_session = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)
    async with async_session() as session:
        yield session

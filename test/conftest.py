import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from ..app.main import app
from ..app.handlers import get_db
from ..app.database import Base
from ..app.settings import settings

# The argument: connect_args={"check_same_thread": False} is needed only for SQLite.
# It's not needed for other databases.
engine = create_engine(
    settings.test_database_url, connect_args={'check_same_thread': False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='module')
def test_app():
    app.dependency_overrides[get_db] = get_test_db

    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)

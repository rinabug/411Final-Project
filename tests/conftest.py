import pytest
from app import create_app
from app.database import Base, engine, session

@pytest.fixture(scope='session', autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

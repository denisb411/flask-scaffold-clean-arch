import pytest
from sqlalchemy.orm import sessionmaker, scoped_session
from app.config import db
from app.main import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app()
    return app


@pytest.fixture
def db_session(app):
    """Creates a scoped session that rolls back after each test."""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()

        session_factory = sessionmaker(bind=connection)
        session = scoped_session(session_factory)

        db.session = session  # override the global session
        yield session

        transaction.rollback()
        connection.close()
        session.remove()


@pytest.fixture
def client(app, db_session):
    """Yields a test client using the test-scoped DB session."""
    return app.test_client()

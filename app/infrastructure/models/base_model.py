from app.config import db

class Base(db.Model):  # type: ignore[name-defined]
    """
    Base model for all ORM classes using Flask-SQLAlchemy.
    """
    __abstract__ = True
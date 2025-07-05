import os
from flask_sqlalchemy import SQLAlchemy

DATABASE_URL = os.environ.get("DATABASE_URL")
print(f"Connecting to database: {DATABASE_URL}")
db = SQLAlchemy()
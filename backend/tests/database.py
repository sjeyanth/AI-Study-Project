from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import TEST_DATABASE_URL

engine = create_engine(
    TEST_DATABASE_URL
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
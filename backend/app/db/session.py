from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings


# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,  # Verifies connections before using them
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    Dependency function that provides database sessions.
    Usage: db = next(get_db())
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings


# Get database URL from settings (reads from .env or Railway)
DATABASE_URL = settings.DATABASE_URL

# Railway uses postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create database engine
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """Dependency function that provides database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
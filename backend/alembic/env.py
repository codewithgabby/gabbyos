from logging.config import fileConfig
import sys
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your models' Base metadata
from app.db.base import Base
target_metadata = Base.metadata

# Import all models so Alembic detects them
from app.models.user import User
from app.models.category import Category
from app.models.routine import Routine
from app.models.weekly_plan import WeeklyPlan, WeeklyPlanItem
from app.models.daily_log import DailyLog
from app.models.streak import Streak
from app.models.reflection import Reflection
from app.models.goal import Goal
from app.models.inbox_item import InboxItem
from app.models.knowledge_item import KnowledgeItem
from app.models.project import Project
from app.models.project_task import ProjectTask


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
from logging.config import fileConfig
import asyncio

from sqlalchemy import pool
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
from app.core.database import Base
from app.models import user_model
target_metadata = Base.metadata


def run_migrations_offline() -> None:
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
    """Run migrations in 'online' mode using an async engine.

    This uses SQLAlchemy's async engine and calls the synchronous
    Alembic migration functions inside `connection.run_sync(...)`.
    """
    connectable = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
    )

    def do_run_migrations(sync_connection):
        context.configure(connection=sync_connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

    async def run_async_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

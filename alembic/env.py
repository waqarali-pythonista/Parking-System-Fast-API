# alembic/env.py

import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import Base
from app.models import user, parking_area, booking  # Import all models to ensure they are registered
from app.core.config import SQLALCHEMY_DATABASE_URL

# Alembic configuration setup
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers, so it's important to have it configured correctly.
fileConfig(config.config_file_name)

# Add your model's MetaData object here
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = SQLALCHEMY_DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    # This part creates an engine and binds it to the context
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )
    
    with engine.connect() as connection:
        # Bind the connection to the context
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Choose which mode to run based on whether we are running offline or online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

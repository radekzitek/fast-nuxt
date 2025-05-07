from logging.config import fileConfig
import os # Add this import
import sys # Add this import

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# This line allows alembic to find your app modules
# Assuming your alembic.ini and env.py are in a directory at the same level as 'app'
# or if you run alembic from the 'backend' directory.
# If your project structure is different, you might need to adjust this.
# For example, if 'alembic' is inside 'app', this might not be needed or different.
# Given your structure where 'alembic' and 'app' are siblings under 'backend',
# and if you run alembic from 'backend', '.' should be sufficient if added to sys.path.
# The `prepend_sys_path = .` in alembic.ini should handle this.
# For robustness, explicitly add the parent directory of 'app'
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


# Import your app's Base and settings
from app.db.base_class import Base  # Import your Base
from app.core.config import settings # Import your settings

# === Add this section to import your models ===
# This ensures that your models are registered with Base.metadata
# before Alembic's autogenerate process uses it.
# import app.models.user
# If you have other model files, import them here as well:
# e.g., import app.models.item
# ============================================

# === Import your models package ===
# This ensures that all models imported in app/models/__init__.py
# are registered with Base.metadata before Alembic uses it.
import app.models
# ==================================

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the sqlalchemy.url from your application settings
# This overrides the sqlalchemy.url from alembic.ini
config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URL)


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata # Point to your Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Include user-defined types for SQLite if necessary, e.g. for JSON
        # render_item=render_item_sqlite,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}), # Uses sqlalchemy.url from config
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
            # Include user-defined types for SQLite if necessary
            # render_item=render_item_sqlite,
        )

        with context.begin_transaction():
            context.run_migrations()

# Optional: for SQLite, if you use types not natively supported by autogenerate (e.g. JSON)
# you might need a render_item function. For basic types, this is not usually needed.
# def render_item_sqlite(type_, obj, autogen_context):
#     """Render an item for SQLite if it's a type that needs special handling."""
#     if type_ == 'type' and isinstance(obj, sa.JSON):
#         # Import your custom JSON type if you have one, or handle as needed
#         autogen_context.imports.add("import sqlalchemy as sa")
#         return "sa.JSON"
#     return False # Let Alembic handle other types


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
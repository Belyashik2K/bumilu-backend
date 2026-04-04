import asyncio
import os
from logging.config import fileConfig
from typing import Any

import alembic_postgresql_enum  # noqa: F401
from alembic import context
from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

import app.core.infrastructure.database.models_registry  # noqa: F401
from app.core.infrastructure.database import BaseModel

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseModel.metadata

load_dotenv()
config.set_main_option("sqlalchemy.url", os.environ["ALEMBIC__DATABASE_URL"])

OWN_TABLES = set(target_metadata.tables.keys())

EXCLUDED_TABLES = {
    "spatial_ref_sys",
    "geometry_columns",
    "geography_columns",
    "raster_columns",
    "raster_overviews",
    "topology",
    "layer",
    "addr",
    "addrfeat",
    "bg",
    "county",
    "countysub",
    "cousub",
    "direction_lookup",
    "edges",
    "faces",
    "featnames",
    "geocode_settings",
    "geocode_settings_default",
    "county_lookup",
    "countysub_lookup",
    "place",
    "place_lookup",
    "secondary_unit_lookup",
    "state",
    "state_lookup",
    "street_type_lookup",
    "tabblock",
    "tabblock20",
    "tract",
    "zcta5",
    "zip_lookup",
    "zip_lookup_all",
    "zip_lookup_base",
    "zip_state",
    "zip_state_loc",
    "pagc_gaz",
    "pagc_lex",
    "pagc_rules",
    "loader_lookuptables",
    "loader_platform",
    "loader_variables",
}

EXCLUDED_SCHEMAS = {"tiger", "tiger_data", "topology"}


def _get_parent_table_info(object_, type_):
    if type_ == "table":
        return getattr(object_, "schema", None), getattr(object_, "name", None)

    table = getattr(object_, "table", None)
    if table is None:
        table = getattr(getattr(object_, "parent", None), "table", None)

    if table is not None:
        return getattr(table, "schema", None), getattr(table, "name", None)

    return None, None


def include_object(object_, name: Any, type_: Any, reflected: Any, compare_to: Any) -> bool:
    schema, table_name = _get_parent_table_info(object_, type_)

    if schema in EXCLUDED_SCHEMAS:
        return False
    if name in EXCLUDED_TABLES or table_name in EXCLUDED_TABLES:
        return False
    return True


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=include_object,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

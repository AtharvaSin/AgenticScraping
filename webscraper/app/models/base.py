"""SQLAlchemy database setup and dynamic model helpers."""

import os
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    MetaData,
    Table,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import registry

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db/postgres")
engine = create_engine(DATABASE_URL)
mapper_registry = registry()
metadata = mapper_registry.metadata


def create_table(table_name: str):
    cols = [
        Column("id", Integer, primary_key=True),
        Column("url", String, nullable=False),
        Column("scraped_at", DateTime, default=datetime.utcnow),
        Column("payload", JSONB),
    ]
    table = Table(table_name, metadata, *cols)
    metadata.create_all(engine, tables=[table])
    return table


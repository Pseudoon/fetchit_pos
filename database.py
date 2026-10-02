import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Reads DATABASE_URL from the environment when deployed (e.g. a hosted Postgres
# connection string from Render/Railway), and falls back to a local SQLite file
# for running on your own machine. No code change needed between the two.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./fetchit.db")

# Render/Railway/Neon sometimes hand out URLs starting with postgres:// — SQLAlchemy
# needs postgresql:// instead.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Explicitly pin the driver to psycopg2 (matches psycopg2-binary in requirements.txt).
# Without this, newer SQLAlchemy versions can default to the psycopg (v3) driver
# instead, which isn't installed, and the app crashes on startup with
# "ModuleNotFoundError: No module named 'psycopg'".
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_auto_migrations():
    """
    Lightweight auto-migration: compares each model's columns against what's
    actually in the SQLite file, and ADDs any missing columns instead of
    requiring you to delete fetchit.db every time a model changes.

    Limitations: only handles ADDING new columns (fine for this project's
    needs). Renaming/removing columns still needs a manual fix or a real
    migration tool (Alembic) if the project grows.
    """
    from sqlalchemy import inspect, text

    inspector = inspect(engine)

    with engine.begin() as conn:
        for table_name, table in Base.metadata.tables.items():
            if not inspector.has_table(table_name):
                continue  # brand-new table — create_all already handled it

            existing_columns = {col["name"] for col in inspector.get_columns(table_name)}

            for column in table.columns:
                if column.name in existing_columns:
                    continue

                col_type = column.type.compile(dialect=engine.dialect)
                default_clause = ""
                if column.default is not None and getattr(column.default, "is_scalar", False):
                    val = column.default.arg
                    if isinstance(val, str):
                        default_clause = f" DEFAULT '{val}'"
                    elif isinstance(val, (int, float)):
                        default_clause = f" DEFAULT {val}"

                ddl = f"ALTER TABLE {table_name} ADD COLUMN {column.name} {col_type}{default_clause}"
                conn.execute(text(ddl))
                print(f"[auto-migrate] added missing column: {table_name}.{column.name}")
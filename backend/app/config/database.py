import logging
import asyncpg
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config.settings import settings
from app.db.models import Base

logger = logging.getLogger("uvicorn.error")

class Database:
    engine = None
    session_factory = None
    in_memory_store = {
        "users": {},
        "reports": {},
        "medicines": {},
        "reminder_history": []
    }
    is_connected = False

db_instance = Database()

async def ensure_database_exists():
    try:
        sys_conn = await asyncpg.connect(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_SERVER,
            port=settings.POSTGRES_PORT,
            database="postgres",
            timeout=5
        )
        db_exists = await sys_conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", settings.POSTGRES_DB
        )
        if not db_exists:
            logger.info(f"Database '{settings.POSTGRES_DB}' does not exist on PostgreSQL server. Creating database automatically...")
            await sys_conn.execute(f'CREATE DATABASE "{settings.POSTGRES_DB}"')
            logger.info(f"Database '{settings.POSTGRES_DB}' created successfully in PostgreSQL.")
        await sys_conn.close()
    except Exception as e:
        logger.debug(f"Database auto-creation check skipped: {str(e)}")

async def connect_to_postgres():
    try:
        # First ensure target database exists in PostgreSQL
        await ensure_database_exists()

        url = settings.async_database_url
        db_instance.engine = create_async_engine(
            url,
            echo=False,
            future=True,
            connect_args={"timeout": 5}
        )
        db_instance.session_factory = async_sessionmaker(
            bind=db_instance.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

        # Test connection & auto-create tables
        async with db_instance.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
            # Auto-migrate missing columns and expand column types in pre-existing PostgreSQL tables
            migrations = [
                "ALTER TABLE reports ADD COLUMN IF NOT EXISTS file_name VARCHAR(500)",
                "ALTER TABLE reports ADD COLUMN IF NOT EXISTS raw_text TEXT",
                "ALTER TABLE health_records ALTER COLUMN id TYPE VARCHAR(255)",
                "ALTER TABLE health_records ALTER COLUMN report_id TYPE VARCHAR(255)",
                "ALTER TABLE reports ALTER COLUMN id TYPE VARCHAR(255)",
                "ALTER TABLE users ALTER COLUMN id TYPE VARCHAR(255)",
                "ALTER TABLE medicines ALTER COLUMN id TYPE VARCHAR(255)",
                "ALTER TABLE reminder_history ALTER COLUMN id TYPE VARCHAR(255)",
            ]
            for query in migrations:
                try:
                    await conn.execute(text(query))
                except Exception as ex:
                    logger.debug(f"Migration statement skipped: {query} -> {ex}")

        db_instance.is_connected = True
        logger.info(f"Successfully connected to PostgreSQL database: '{settings.POSTGRES_DB}' at {settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}")
    except Exception as e:
        logger.warning(
            f"Could not connect to PostgreSQL database ({str(e)}). "
            f"Ensure PostgreSQL service is running and credentials in backend/.env are correct. "
            f"Fallback in-memory store initialized."
        )
        db_instance.is_connected = False
        db_instance.engine = None
        db_instance.session_factory = None

async def close_postgres_connection():
    if db_instance.engine:
        await db_instance.engine.dispose()
        logger.info("Closed PostgreSQL connection engine.")

async def get_db_session() -> AsyncSession:
    if db_instance.session_factory:
        async with db_instance.session_factory() as session:
            yield session
    else:
        yield None

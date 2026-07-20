import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

logger = logging.getLogger("uvicorn.error")

class Database:
    client: AsyncIOMotorClient = None
    db = None
    in_memory_store = {"users": {}}
    is_connected = False

db_instance = Database()

async def connect_to_mongo():
    try:
        db_instance.client = AsyncIOMotorClient(
            settings.MONGODB_URL, 
            serverSelectionTimeoutMS=2000
        )
        # Verify connection
        await db_instance.client.admin.command('ping')
        db_instance.db = db_instance.client[settings.DATABASE_NAME]
        db_instance.is_connected = True
        logger.info(f"Connected to MongoDB database: '{settings.DATABASE_NAME}' at {settings.MONGODB_URL}")
    except Exception as e:
        logger.warning(f"Could not connect to MongoDB server at {settings.MONGODB_URL} ({str(e)}). Fallback store initialized.")
        db_instance.is_connected = False
        db_instance.db = None

async def close_mongo_connection():
    if db_instance.client:
        db_instance.client.close()
        logger.info("Closed MongoDB connection.")

def get_database():
    return db_instance.db

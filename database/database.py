from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings
import pymongo

# Configuración de MongoDB
MONGO_URI = "mongodb+srv://USR-Multimedia:Multi12345@cluster0.utjyivv.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "USR-Multimedia"

mongo_client = pymongo.MongoClient(MONGO_URI)
db_mongo = mongo_client[DB_NAME]

def get_mongo_collection(collection_name: str):
    return db_mongo[collection_name]

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


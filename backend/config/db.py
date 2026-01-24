import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# This line finds the .env file and loads it into your system's memory
load_dotenv()

# Now you pull the values out using os.getenv
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = AsyncIOMotorClient(MONGO_URL)
database = client[DB_NAME]
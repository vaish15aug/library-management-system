
import os
from dotenv import load_dotenv

load_dotenv()

# sqlDBUrl = os.getenv("SQL_DB_URL")
db_user = os.getenv("DB_USER")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_password= os.getenv("DB_PASSWORD")                  
mongoUri = os.getenv("MONGO_URI")
jwtSecret = os.getenv("JWT_SECRET_KEY")
jwtAlgorithm = os.getenv("JWT_ALGORITHM")
redisHost = os.getenv("REDIS_HOST")
redisPort = os.getenv("REDIS_PORT")

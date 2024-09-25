from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from helpers.envVars import db_password, db_host, db_name, db_port, db_user


# DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/library')
DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL)
print("engine", engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print("local session", SessionLocal)
Base = declarative_base()

def getDb():
    try:
        db: Session = SessionLocal()
        print("db", db)
        return db
    except Exception as e:
        raise Exception("error connection to DB", str(e))
    finally:
        db.close()



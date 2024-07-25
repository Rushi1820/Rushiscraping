from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

DATABASE_URL = "postgresql://scrapingdatabase_user:P7dMq2qFg3t0pVrDUVWgWL30liTi9IET@dpg-cqgt4p2ju9rs73ebui8g-a.singapore-postgres.render.com/scrapingdatabase"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
database = Database(DATABASE_URL)
Base = declarative_base()


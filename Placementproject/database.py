from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

DATABASE_URL = "postgresql://rushi:GHdFDzD5lHwS4YUbOfMY7x3jmmOPzXEH@dpg-cvl14r3uibrs73a7r2dg-a.oregon-postgres.render.com/jobscraper"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
database = Database(DATABASE_URL)
Base = declarative_base()


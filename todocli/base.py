"""Base for database connections."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from todocli.config import CONFIG

engine = create_engine(CONFIG['db_dialect'], echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()

# shared/db.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

user = os.getenv("MYSQL_USER", "root")
pwd  = os.getenv("MYSQL_PASSWORD", "")
host = os.getenv("MYSQL_HOST", "localhost")
port = os.getenv("MYSQL_PORT", "3306")
db   = os.getenv("MYSQL_DATABASE", "InvoiceDB")

DATABASE_URL = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}"

engine = create_engine(DATABASE_URL, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

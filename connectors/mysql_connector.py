from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')

if not all([username, password, host, database]):
    raise ValueError("Database credentials are not properly set.")

# Connect to the database
print("Connecting to the MySQL Database")
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database}')

# Test the connection
try:
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    print(f'Connected to the MySQL Database at {host}')
except Exception as e:
    print(f"Failed to connect to the database: {e}")

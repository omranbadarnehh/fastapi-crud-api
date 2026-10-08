from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal =  sessionmaker(autocommit=False , autoflush=False ,bind=engine)

Base = declarative_base()

def get_dp():
    dp = SessionLocal()
    try :
        yield dp
    finally :
        dp.close()




# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password="Qwer1234",
#             port=5433,
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("connection to Database failed")
#         print("error was", error)
#         time.sleep(2)

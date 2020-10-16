from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

path = os.path.dirname(os.path.realpath(__file__))
database_path = os.path.join(path, 'mydb.sqlite')
SQLALCHEMY_DATABASE_URI = f'sqlite:////{database_path}'
MYSQL_CHARSET = 'utf8mb4'  # emoji compatibility

engine = create_engine(
    SQLALCHEMY_DATABASE_URI
)

Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)

print('declaring Base')
Base = declarative_base()

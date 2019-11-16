from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)

class Log(Base):
    __tablename__ = 'logs'

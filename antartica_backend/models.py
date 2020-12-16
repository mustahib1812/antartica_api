import datetime
from django.conf import settings

from sqlalchemy import CHAR, Column, DECIMAL, Date, DateTime, Enum, Float, ForeignKey, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER, LONGTEXT, MEDIUMTEXT, SMALLINT, TINYINT

from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Employees(Base):
    __tablename__ = 'employees'

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False)
    password = Column(String(255), nullable=False)
    organization_name = Column(String(255), nullable=False)
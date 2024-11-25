from enum import unique

# # Пользователи нашего сайта

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase
from ormbase import db  # Предполагаем, что SQLAlchemy инициализирован



class Property(SqlAlchemyBase):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    location = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    comments = orm.relationship('Comment', back_populates='property')
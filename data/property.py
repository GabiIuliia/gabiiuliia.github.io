# Пользователи нашего сайта

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Property(SqlAlchemyBase):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    location = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    comments = orm.relationship('Comment', back_populates='property')

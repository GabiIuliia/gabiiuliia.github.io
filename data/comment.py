from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy import orm
from datetime import datetime

from data.db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    property_id = Column(Integer, ForeignKey('properties.id'))
    user = orm.relationship('User', back_populates='comments')
    property = orm.relationship('Property', back_populates='comments')
from enum import unique

import sqlalchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from main import index
from ormbase import db  # Предполагаем, что SQLAlchemy инициализирован

# from .db_session import SqlAlchemyBase
#
# # роль пользователя
# ACCESS = {
#     'user': 1,
#     'admin': 2
# }


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    comments = relationship('Comment', back_populates='user')
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now())
    news = orm.relationship("News", back_populates='user')
 #
 #    def __repr__(self):
 #        return f'<Объект user, пользователь {self.name}>'
 #
 #    def __str__(self):
 #        return f'<Объект user, пользователь {self.name}>'
 #
 #    def set_password(self, password):
 #        self.hashed_password = generate_password_hash(password)
 #
 #    def check_password(self, password):
 #        return check_password_hash(self.hashed_password, password)

class Property(db.Model):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    location = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    comments = relationship('Comment', back_populates='property')

class Comment(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    property_id = Column(Integer, ForeignKey('properties.id'))
    user = relationship('User', back_populates='comments')
    property = relationship('Property', back_populates='comments')

# # Новости нашего сайта
# import datetime
# import sqlalchemy
# from sqlalchemy import orm
# from .db_session import SqlAlchemyBase
#
#
# class News(SqlAlchemyBase):
#     __tablename__ = 'news'
#
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
#                            autoincrement=True)
#     title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
#     content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
#     create_date = sqlalchemy.Column(sqlalchemy.DateTime,
#                                     default=datetime.datetime.now())
#     is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
#     user_id = sqlalchemy.Column(sqlalchemy.Integer,
#                                 sqlalchemy.ForeignKey("users.id"))
#     user = orm.relationship('User')
#
#     def __repr__(self):
#         return f'<Объект news, новость {self.id}>'
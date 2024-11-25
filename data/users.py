from enum import unique

# # Пользователи нашего сайта

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import sqlalchemy.orm as orm
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase
from ormbase import db  # Предполагаем, что SQLAlchemy инициализирован






# роль пользователя
ACCESS = {
    'user': 1,
    'admin': 2
}

class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = Column(sqlalchemy.Integer, primary_key=True,
                autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    level = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.now())
    comments = orm.relationship('Comment', back_populates='user')
    news = orm.relationship("News", back_populates='user')

    #
    def __repr__(self):
        return f'<Объект user, пользователь {self.email}, {self.password_hash}>'

    def __str__(self):
        return f'<Объект user, пользователь {self.email}, {self.password_hash}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id

    # Является ли текущий пользователь админом
    def is_admin(self):
        return self.level == ACCESS['admin']

    # Разрешён ли доступ пользователья с текущим уровнем
    def allowed(self, access_level):
        return self.level >= access_level



#
#
# class User(SqlAlchemyBase, UserMixin, SerializerMixin):
#     __tablename__ = 'users'
#
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
#                            autoincrement=True)
#     name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
#     about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
#     email = sqlalchemy.Column(sqlalchemy.String, index=True,
#                               unique=True, nullable=True)
#     # level = sqlalchemy.Column(sqlalchemy.Integer, default=1)
#     hashed_password = sqlalchemy.Column(sqlalchemy.String,
#                                         nullable=True)
#     created_date = sqlalchemy.Column(sqlalchemy.DateTime,
#                                      default=datetime.datetime.now())
#
#     news = orm.relationship("News", back_populates='user')
#



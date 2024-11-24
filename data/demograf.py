from enum import unique

# # Пользователи нашего сайта
# import datetime
import sqlalchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
# с 10
# from flask_login import UserMixin
# from sqlalchemy import orm
# from werkzeug.security import generate_password_hash, check_password_hash
#
# from .db_session import SqlAlchemyBase
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from main import index
from ormbase import db  # Предполагаем, что SQLAlchemy инициализирован


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


# ORM - Object Relational Mapping - объектно-реляционное отображение
# pip install sqlalchemy


SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл БД при вызове global_init")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f'Мы подключились к БД по адресу: {conn_str}')

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
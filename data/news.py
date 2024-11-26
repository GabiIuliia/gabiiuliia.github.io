# Новости нашего сайта
import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase
from .users import User  # Импортируем класс User


class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                    default=datetime.datetime.now())
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')

    def __repr__(self):
        return f'<Объект news, новость {self.id}>'
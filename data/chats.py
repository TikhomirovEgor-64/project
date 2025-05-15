import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Chats(SqlAlchemyBase, UserMixin):
    __tablename__ = 'chats'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    first = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    second = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    chat = sqlalchemy.Column(sqlalchemy.String, default='&')

    users3 = orm.relationship("Users", foreign_keys=[first], back_populates="chats1")
    users4 = orm.relationship("Users", foreign_keys=[second], back_populates="chats2")

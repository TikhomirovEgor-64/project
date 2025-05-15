import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Requests(SqlAlchemyBase, UserMixin):
    __tablename__ = 'requests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    first = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    second = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    users1 = orm.relationship("Users", foreign_keys=[first], back_populates="requests1")
    users2 = orm.relationship("Users", foreign_keys=[second], back_populates="requests2")

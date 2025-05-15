import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Users(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname1 = sqlalchemy.Column(sqlalchemy.String)
    surname2 = sqlalchemy.Column(sqlalchemy.String)
    photo = sqlalchemy.Column(sqlalchemy.String, default='default_image_profile.png')
    date_of_birth = sqlalchemy.Column(sqlalchemy.DateTime)
    info_about = sqlalchemy.Column(sqlalchemy.String, default='(отсутствует)')

    requests1 = orm.relationship("Requests",
                                 foreign_keys="[Requests.first]",
                                 back_populates="users1")
                               
    requests2 = orm.relationship("Requests",
                                 foreign_keys="[Requests.second]",
                                 back_populates="users2")
    
    chats1 = orm.relationship("Chats",
                              foreign_keys="[Chats.first]",
                              back_populates="users3")
                                 
    chats2 = orm.relationship("Chats",
                              foreign_keys="[Chats.second]",
                              back_populates="users4")

    history = orm.relationship("History", back_populates='users5')
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

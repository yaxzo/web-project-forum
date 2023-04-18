import datetime
from flask_login import UserMixin

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase

from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String,
                                 index=True,
                                 unique=True,
                                 nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True,
                              unique=True,
                              nullable=False)
    profile_photo = sqlalchemy.Column(sqlalchemy.String,
                                      default="default.webp",
                                      nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String,
                                        nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.date.today())

    trads = orm.relationship("Trad", back_populates="user", lazy=True)
    article = orm.relationship("Article", back_populates="user", lazy=True)
    comments = orm.relationship("TradComment", back_populates="user", lazy=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

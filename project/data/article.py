import datetime

from flask_login import UserMixin

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Article(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "articles"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String,
                              nullable=False)
    preview = sqlalchemy.Column(sqlalchemy.String,
                                nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String,
                                nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("users.id"))
    trad_photo = sqlalchemy.Column(sqlalchemy.String,
                                   default="default.webp",
                                   nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.date.today())
    is_private = sqlalchemy.Column(sqlalchemy.Boolean,
                                   nullable=False)
    user = orm.relationship("User")


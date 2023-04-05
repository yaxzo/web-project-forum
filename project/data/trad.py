import datetime

from flask_login import UserMixin

import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Trad(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "trads"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String,
                              nullable=False)
    preview = sqlalchemy.Column(sqlalchemy.String,
                                nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String,
                                nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.date.today())
    is_private = sqlalchemy.Column(sqlalchemy.Boolean,
                                   nullable=False)

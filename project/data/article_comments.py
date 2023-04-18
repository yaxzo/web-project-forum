from flask_login import UserMixin

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class ArticleComment(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "article_comments"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("users.id"))
    article_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("trads.id", ondelete="CASCADE"),
                                   nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String,
                                nullable=False)
    user = orm.relationship("User")

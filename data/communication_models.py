import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Chat(SqlAlchemyBase):
    __tablename__ = 'chats'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user1_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user2_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now().replace(microsecond=0))

    user1 = orm.relationship('User', foreign_keys=user1_id)
    user2 = orm.relationship('User', foreign_keys=user2_id)
    messages = orm.relationship('Message', back_populates='chat', cascade='all, delete-orphan')

class Message(SqlAlchemyBase):
    __tablename__ = 'messages'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now().replace(microsecond=0))

    chat_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("chats.id"))

    chat = orm.relationship('Chat', back_populates='messages')
    user = orm.relationship('User')
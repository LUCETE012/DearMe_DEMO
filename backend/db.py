from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import pytz
from datetime import datetime

db = SQLAlchemy()

KST = pytz.timezone('Asia/Seoul')

def current_time_kst():
    return datetime.now(KST)

class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(30), nullable=False)
    feedId = db.Column(db.Integer, nullable=False)
    feed = db.Column(db.Text, nullable=True)
    feedTime = db.Column(db.DateTime, nullable=True)
    state = db.Column(db.Integer, nullable=True)
    image_path = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Element('{self.user_id}', '{self.feedId}', '{self.feed}', '{self.image_path}', '{self.content}')"

    def serialize_feed(self):
        return {
            "id": self.id,
            "feedId": self.feedId,
            "feed": self.feed,
            "feedTime": self.feedTime,
            "image_path": self.image_path,
        }


from enum import Enum


class SenderEnum(Enum):
    user = 0
    assistant = 1
    system = 2
    photo = 3


class User(db.Model):
    __tablename__ = "user"
    UId = db.Column(db.String, primary_key=True)
    UName = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False)
    Persona = db.Column(db.Text, nullable=True)

    Chats = db.relationship("Chat", backref="user", lazy=True)


class Chat(db.Model):
    __tablename__ = "chat"
    ChatId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UId = db.Column(db.Integer, db.ForeignKey("user.UId"), nullable=False)
    Date = db.Column(db.DateTime, default=current_time_kst, nullable=False)

    Messages = db.relationship("Message", backref="chat", lazy=True)
    Diary = db.relationship("Diary", backref="chat", lazy=True)


class Message(db.Model):
    __tablename__ = "message"
    MessageId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ChatId = db.Column(db.Integer, db.ForeignKey("chat.ChatId"), nullable=False)
    Message = db.Column(db.Text, nullable=False)
    Sender = db.Column(db.Enum(SenderEnum), nullable=False)
    Time = db.Column(db.Time, nullable=False)

    def serialize(self):
        return {
            "MessageId": self.MessageId,
            "ChatId": self.ChatId,
            "content": self.Message,
            "role": self.Sender.name,
            "time": self.Time.strftime("%H:%M:%S"),
        }

    def serialize_for_ai(self):
        return {
            "role": self.Sender.name,
            "content": self.Message,
        }


class Diary(db.Model):
    __tablename__ = "diary"
    DiaryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ChatId = db.Column(db.Integer, db.ForeignKey("chat.ChatId"), nullable=False)
    Content = db.Column(db.Text, nullable=True)
    ImgURL = db.Column(db.String, nullable=True)
    CreatedAt = db.Column(db.DateTime, default=current_time_kst, nullable=False)
    UpdatedAt = db.Column(
        db.DateTime, default=current_time_kst, onupdate=current_time_kst, nullable=False
    )

    def serialize(self):
        return {
            "id": self.DiaryId,
            "content": self.Content,
            "created_at": self.CreatedAt,
            "updated_at": self.UpdatedAt,
            "img_url": self.ImgURL,
        }
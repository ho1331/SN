from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.app import db


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    date = db.Column(db.Date, unique=False, nullable=False)


class LikeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Like
        include_fk = True


class LikeCountSchema(Schema):
    date = fields.String()
    likes_count = fields.Int()

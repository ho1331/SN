from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.app import db


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    date = db.Column(db.DateTime, unique=False, nullable=False)


class LikeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Like
        include_fk = True

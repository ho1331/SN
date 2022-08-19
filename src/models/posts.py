from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.app import db


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('Like', cascade='all,delete', backref='post', lazy='dynamic')


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post

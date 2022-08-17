from datetime import datetime

# from flask_login import UserMixin
from sqlalchemy.orm import validates
from src.app import db

from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    posts = db.relationship("Post", backref="user")
    liked = db.relationship('Like', secondary="likes", backref='user')
    disliked = db.relationship('DisLike', secondary="dislikes", backref='user')
    # liked = db.relationship(
    #     'Like',
    #     foreign_keys='Like.users_id',
    #     backref='users', lazy='dynamic')
    # disliked = db.relationship(
    #     'DisLike',
    #     foreign_keys='DisLike.users_id',
    #     backref='users', lazy='dynamic')

    @validates("email")
    def validate_rating(self, key, field):
        """
        Check email input
        """
        if "@" in field:
            return field
        else:
            raise AssertionError("Bad field : 'email'")

    def __init__(
        self,
        name: str,
        username: str,
        email: str,
        password: str,
        is_admin: bool = False,
    ) -> None:
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def set_password(self, password):
        """
        set hash password
        """
        self.pswhash = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """
        check password
        """
        return check_password_hash(self.pswhash, password)

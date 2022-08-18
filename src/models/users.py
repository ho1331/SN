from datetime import datetime

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash

from src.app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    posts = db.relationship('Post', backref='user')
    liked = db.relationship(
        'Like',
        foreign_keys='Like.user_id',
        backref='user', lazy='dynamic')

    @validates('email')
    def validate_rating(self, key, field):
        """
        Check email input
        """
        if '@' in field:
            return field
        else:
            raise AssertionError('Bad field : \'email\'')

    def set_password(self, password):
        """
        set hash password
        """
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """
        check password
        """
        return check_password_hash(self.password, password)


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User

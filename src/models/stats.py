from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.app import db


class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    logged = db.Column(db.DateTime, unique=False, nullable=False)
    last_request_at = db.Column(db.DateTime, unique=False, nullable=False)


class StatsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Stats

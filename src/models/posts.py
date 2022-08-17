from src.app import db


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(150), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title: str) -> None:
        self.title = title

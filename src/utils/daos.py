import logging

from sqlalchemy.exc import NoResultFound

from src.app import db
from src.models.likes import Like
from src.models.posts import Post
from src.models.users import User


class ModelDAO:
    def __init__(self, model):
        self.model = model

    def get_new(self):
        return self.model()

    def get_all(self):
        item = db.session.query(self.model).all()
        return item

    def get_by_id(self, item_id):
        try:
            return db.session.query(self.model).filter_by(id=item_id).first()
        except NoResultFound:
            return None

    def del_by_id(self, item_id):
        item = db.session.query(self.model).get_or_404(item_id, 'Not Found')
        db.session.delete(item)
        db.session.commit()

        return item


class UserDAO(ModelDAO):
    def create_user(self, data):
        result = None

        try:
            user = self.get_new()
            user.name = data['name']
            user.username = data['username']
            user.email = data['email']
            user.set_password(data['password'])

            db.session.add(user)
            db.session.commit()
            result = user

        except Exception as exception:
            logging.error(exception)
            db.session.rollback()

        return result

    def get_by_email(self, email):
        try:
            return db.session.query(self.model).filter_by(email=email).first()
        except NoResultFound:
            return None

    def get_by_username(self, username):
        try:
            return db.session.query(self.model).filter_by(username=username).first()
        except NoResultFound:
            return None


class PostDAO(ModelDAO):
    def create_post(self, data, user_id):
        result = None

        try:
            post = self.get_new()
            post.title = data['title']
            post.user_id = user_id

            db.session.add(post)
            db.session.commit()
            result = post

        except Exception as exception:
            logging.error(exception)
            db.session.rollback()

        return result


class LikeDAO(ModelDAO):
    def like(self, data, user_id):
        result = None

        try:
            like = self.get_new()
            exist = db.session.query(self.model).filter_by(
                user_id=user_id,
                post_id=data['post_id']).first()

            if exist:
                db.session.delete(exist)
                db.session.commit()
                return

            like.post_id = data['post_id']
            like.user_id = user_id

            db.session.add(like)
            db.session.commit()
            result = like

        except Exception as exception:
            logging.error(exception)
            db.session.rollback()

        return result


user_dao = UserDAO(User)
post_dao = PostDAO(Post)
like_dao = LikeDAO(Like)

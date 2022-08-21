import logging
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.exc import NoResultFound

from src.app import db
from src.models.likes import Like
from src.models.posts import Post
from src.models.stats import Stats
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
        except NoResultFound as e:
            raise e

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
            user.email = data['email']
            user.set_password(data['password'])

            db.session.add(user)
            db.session.commit()
            result = user

        except Exception as exception:
            logging.error(exception)
            db.session.rollback()
            raise exception

        return result

    def get_by_email(self, email):
        try:
            return db.session.query(self.model).filter_by(email=email).first()
        except NoResultFound as e:
            raise e


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

        except Exception as e:
            logging.error(e)
            db.session.rollback()
            raise e

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
            like.date = datetime.now()

            db.session.add(like)
            db.session.commit()
            result = like

        except Exception as e:
            logging.error(e)
            db.session.rollback()
            raise e

        return result

    def get_like_stat(self, start_date=None, end_date=None):
        result = None

        try:
            if start_date and end_date:
                exist = db.session.query(self.model.date, func.count(self.model.date).label('likes_count')).group_by(self.model.date).all()
            elif start_date:
                exist = db.session.query(self.model).filter(self.model.date >= start_date).all()
            else:
                exist = db.session.query(self.model).filter(self.model.date <= end_date).all()
            result = exist

        except Exception as e:
            logging.error(e)
            raise e

        return result


class UserStatsDAO(ModelDAO):
    def update_stat(self, user_id, login=True):
        result = None

        try:
            stat = self.get_new()
            exist = db.session.query(self.model).filter_by(
                user_id=user_id).first()

            if exist and login:
                exist.logged = datetime.now()
                exist.last_request_at = datetime.now()
                db.session.add(exist)
                db.session.commit()
                return
            elif exist and not login:
                exist.last_request_at = datetime.now()
                db.session.add(exist)
                db.session.commit()
                return

            stat.user_id = user_id
            stat.logged = datetime.now()
            stat.last_request_at = datetime.now()

            db.session.add(stat)
            db.session.commit()
            result = stat

        except Exception as e:
            logging.error(e)
            db.session.rollback()
            raise e

        return result


user_dao = UserDAO(User)
post_dao = PostDAO(Post)
like_dao = LikeDAO(Like)
user_stat_dao = UserStatsDAO(Stats)

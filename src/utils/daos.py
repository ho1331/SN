from sqlalchemy.exc import NoResultFound
from app import db
import logging


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
            return db.session.query(self.model).filter_by(id=item_id).one()
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
            result = user.id

        except Exception as exception:
            logging.error(exception)

        return result

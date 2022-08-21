from flask import request
from flask_jwt_extended import verify_jwt_in_request
from flask_restx import Api

from src.app import app
from src.utils.daos import user_dao, user_stat_dao

from .auth import api as oauth
from .like import api as likes
from .post import api as posts
from .stat import api as stats
from .user import api as users

api = Api(
    title='Social test API',
    version='1.0',
    doc='/swagger'
)

api.add_namespace(oauth, path='/api')
api.add_namespace(users, path='/api/user')
api.add_namespace(posts, path='/api/post')
api.add_namespace(likes, path='/api/like')
api.add_namespace(stats, path='/api/analytics')


@app.after_request
def after_request_callback(response):
    if 'signup' in request.path:
        pass
    elif 'swagger' in request.path:
        pass
    elif 'user' in request.path and request.method == 'DELETE':
        pass
    elif 'login' not in request.path:
        current_user = verify_jwt_in_request()
        user = user_dao.get_by_email(current_user[1]["sub"])
        user_stat_dao.update_stat(user.id, login=False)
    else:
        data = request.get_json()
        user = user_dao.get_by_email(data['email'])
        user_stat_dao.update_stat(user.id)

    return response

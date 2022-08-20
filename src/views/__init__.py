from flask import request
from flask_jwt_extended import verify_jwt_in_request
from flask_restx import Api
from src.app import app
from src.utils.daos import stat_dao, user_dao

from .like_views import api as like
from .login import api as lg
from .post_views import api as posts
from .signup import api as sinup
from .stats_views import api as stats
from .user_views import api as users

api = Api(
    title='Social test API',
    version='1.0',
    doc='/swagger'
)

api.add_namespace(users, path='/api/user')
api.add_namespace(sinup, path='/api/signup')
api.add_namespace(posts, path='/api/post')
api.add_namespace(lg, path='/api/login')
api.add_namespace(like, path='/api/like')
api.add_namespace(stats, path='/api/analytics/users')


@app.after_request
def after_request_callback(response):
    if 'signup' in request.path:
        pass
    elif 'swagger' in request.path:
        pass
    elif 'login' not in request.path:
        current_user = verify_jwt_in_request()
        user = user_dao.get_by_email(current_user[1]["sub"])
        stat_dao.update_stat(user.id, login=False)
    else:
        data = request.get_json()
        user = user_dao.get_by_email(data['email'])
        stat_dao.update_stat(user.id)

    return response
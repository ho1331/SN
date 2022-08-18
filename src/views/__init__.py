from flask_restx import Api

from .like_views import api as like
from .login import api as lg
from .post_views import api as posts
from .user_views import api as users

api = Api(
    title='Social test API',
    version='1.0'
)

api.add_namespace(users, path='/api/user')
api.add_namespace(posts, path='/api/post')
api.add_namespace(lg, path='/api/login')
api.add_namespace(like, path='/api/like')

from flask_restx import Api

from .user_views import api as users


api = Api(
    title='Users operations',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(users, path='/api/user')

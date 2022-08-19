from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource

from src.models.users import UserSchema
from src.utils.daos import user_dao

api = Namespace('signup', description='SignUp')
user_schema = UserSchema()


@api.route('/')
class SignUpAPI(Resource):
    def post(self):
        data = request.get_json()

        # checking for existing user
        exist_email = user_dao.get_by_email(data['email'])

        if exist_email:
            return make_response(
                jsonify(
                    status_code=200,
                    message='User already exists. Please Log in.'
                    ), 200
            )
        else:
            user_dao.create_user(data)
            return make_response(
                jsonify(
                    message='Successfully registered',
                    status_code=201), 201
            )

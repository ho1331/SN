from flask import jsonify, make_response, request
from flask_jwt_extended import create_access_token
from flask_restx import Namespace, Resource

from src.models.users import UserSchema
from src.utils.daos import user_dao

api = Namespace('auth', description='SignUp')
user_schema = UserSchema()


@api.route('/signup')
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


@api.route('/login')
class LoginAPI(Resource):
    def post(self):
        resp_data = request.get_json()
        try:
            user = user_dao.get_by_email(resp_data.get('email'))
            if user and user.check_password(resp_data.get('password')):
                access_token = create_access_token(identity=resp_data.get('email'))
                if access_token:
                    body = {
                        'status_code': 200,
                        'message': 'Successfully logged in.',
                        'access_token': access_token,
                    }
                    return make_response(jsonify(body), 200)

            else:
                body = {
                    'status_code': 404,
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(body), 404)
        except Exception as e:
            raise e

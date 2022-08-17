from email import message
from flask import request, jsonify, make_response
import jwt
from src.utils.daos import user_dao
from src.models.users import UserSchema
from flask_restx import Resource, Namespace

api = Namespace('users', description='Users related operations')
user_schema = UserSchema()

@api.route('/', '/<int:id>')
class UserAPI(Resource):
    # signup route
    def post(self):
        data = request.get_json()

        # checking for existing user
        exist_user = user_dao.get_by_email(data['email'])
        if not exist_user:
            user_dao.create_user(data)

            return make_response(
                jsonify(
                    message='Successfully registered',
                    status_code=201), 201
            )
        else:
            return make_response(
                jsonify(
                    message='User already exists. Please Log in.',
                    status_code=202), 202
            )
    
    def get(self, id):
        user = user_dao.get_by_id(id)
        print(user)
        if not user:
            return make_response(
                jsonify(
                    message='User doesn\'t exist.',
                    status_code=202), 202
            )
        
        return user_schema.dump(user)

    def delete(self, id):
        user_dao.del_by_id(id)

        return make_response(
            jsonify(
                message='User successfully deleted',
                status_code=200), 200
        )

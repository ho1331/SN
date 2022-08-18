from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from src.models.users import UserSchema
from src.utils.daos import user_dao

api = Namespace('users', description='Users related operations')
user_schema = UserSchema()


@api.route('/', '/<int:id>')
class UserAPI(Resource):
    # signup route
    def post(self):
        data = request.get_json()

        # checking for existing user
        exist_email = user_dao.get_by_email(data['email'])

        if exist_email:
            return make_response(
                jsonify(
                    status_code=202,
                    message='User already exists. Please Log in.'
                    ), 202
            )
        else:
            user_dao.create_user(data)
            return make_response(
                jsonify(
                    message='Successfully registered',
                    status_code=201), 201
            )

    @jwt_required()
    def get(self, id):
        user = user_dao.get_by_id(id)
        if not user:
            return make_response(
                jsonify(
                    message='User doesn\'t exist.',
                    status_code=202), 202
            )

        return user_schema.dump(user)

    @jwt_required()
    def delete(self, id):
        user_dao.del_by_id(id)

        return make_response(
            jsonify(
                message='User successfully deleted',
                status_code=200), 200
        )

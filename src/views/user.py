from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from src.models.users import UserSchema
from src.utils.daos import user_dao

api = Namespace('users', description='Users related operations')
user_schema = UserSchema()


@api.route('/<int:id>')
class UserAPI(Resource):
    @jwt_required()
    def get(self, id):
        user = user_dao.get_by_id(id)
        if not user:
            return make_response(
                jsonify(
                    message='User doesn\'t exist.',
                    status_code=404), 404
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

from flask import jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource

from src.models.likes import LikeSchema
from src.utils.daos import like_dao, user_dao

api = Namespace('likes', description='Likes related operations')
like_schema = LikeSchema()


@api.route('/')
class LikeAPI(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()

        current_user = get_jwt_identity()
        user = user_dao.get_by_email(current_user)
        like = like_dao.like(data, user.id)

        if like:
            return make_response(
                jsonify(
                    message='You liked it',
                    status_code=201), 201
            )
        else:
            return make_response(
                jsonify(
                    message='You disliked it',
                    status_code=204), 204
            )

    @jwt_required()
    def get(self):
        likes = like_dao.get_all()
        if not likes:
            return make_response(
                jsonify(
                    message='Likes doesn\'t exist.',
                    status_code=404), 404
            )
        return like_schema.dump(likes, many=True)

from flask import jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource

from src.models.posts import PostSchema
from src.utils.daos import post_dao, user_dao

api = Namespace('posts', description='Posts related operations')
post_schema = PostSchema()


@api.route('/', '/<int:id>')
class PostAPI(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        current_user = get_jwt_identity()

        user = user_dao.get_by_email(current_user)
        post_dao.create_post(data, user.id)

        return make_response(
            jsonify(
                message='Successfully created',
                status_code=201), 201
        )

    @jwt_required()
    def get(self, id):
        post = post_dao.get_by_id(id)
        if not post:
            return make_response(
                jsonify(
                    message='Post doesn\'t exist.',
                    status_code=404), 404
            )

        return post_schema.dump(post)

    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        user = user_dao.get_by_email(current_user)
        if user.id != id:
            post_dao.del_by_id(id)
        else:
            return make_response(
                jsonify(
                    message='Permission denided',
                    status_code=403), 403
            )
        return make_response(
            jsonify(
                message='Post successfully deleted',
                status_code=200), 200
        )

from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from src.models.likes import LikeSchema
from src.models.stats import StatsSchema
from src.utils.daos import like_dao, user_stat_dao

api = Namespace('stats', description='Analytics dashboard')
stats_schema = StatsSchema()
like_schema = LikeSchema()


@api.route('/users')
class UserStatsAPI(Resource):
    @jwt_required()
    def get(self):
        stats = user_stat_dao.get_all()
        if not stats:
            return make_response(
                jsonify(
                    message='Not Found',
                    status_code=404), 404
            )
        return stats_schema.dump(stats, many=True)


@api.route('/likes')
class LikeStatsAPI(Resource):
    @jwt_required()
    def get(self):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        likes_stat = like_dao.get_like_stat(start_date, end_date)
        if not likes_stat:
            return make_response(
                jsonify(
                    message='Not Found',
                    status_code=404), 404
            )
        return like_schema.dump(likes_stat, many=True)

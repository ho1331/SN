from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from src.models.stats import StatsSchema
from src.utils.daos import stat_dao

api = Namespace('stats', description='Likes related operations')
stats_schema = StatsSchema()


@api.route('/')
class StatsAPI(Resource):
    @jwt_required()
    def get(self):
        stats = stat_dao.get_all()
        if not stats:
            return make_response(
                jsonify(
                    message='Not Found',
                    status_code=404), 404
            )
        return stats_schema.dump(stats, many=True)

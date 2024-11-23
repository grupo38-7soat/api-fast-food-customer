from loguru import logger
from functools import partial
from flask_restx import Namespace, Resource, fields

name_ns = Namespace(name='Nome', description='Descricao')


@name_ns.route('/rota')
class ApiResource(Resource):
    @name_ns.response(200, 'Success', name_ns.model('Validate', {
        'value': fields.String
    }))
    @name_ns.response(500, 'Internal Server Error', name_ns.model('InternalServerError', {
        'message': fields.String
    }))
    def get(self):
        logger.info('api resource')
        return 'data'

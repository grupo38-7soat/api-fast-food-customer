from flask_restx import Namespace, Resource, fields
from loguru import logger

crud_ns = Namespace(name='CRUD', description='CRUD operations')

@crud_ns.route('/create')
class CreateResource(Resource):
    def post(self):
        logger.info('Create resource')
        return {'message': 'Create resource'}, 201

@crud_ns.route('/read')
class ReadResource(Resource):
    def get(self):
        logger.info('Read resource')
        return {'message': 'Read resource'}, 200

@crud_ns.route('/update')
class UpdateResource(Resource):
    def put(self):
        logger.info('Update resource')
        return {'message': 'Update resource'}, 200

@crud_ns.route('/delete')
class DeleteResource(Resource):
    def delete(self):
        logger.info('Delete resource')
        return {'message': 'Delete resource'}, 200
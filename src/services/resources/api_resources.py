from flask_restx import Namespace, Resource, fields
from loguru import logger
from config import Config
from utils.check_document import validate_document
from repository.dynamo_db.dynamo_repository import DynamoRepository

INVALID_CPF = 'Invalid CPF'
AWS_REGION = Config.get('awsRegion')
DYNAMO_TABLE_NAME = Config.get('dynamoTableName')

dynamo_ns = Namespace(name='DynamoCRUD', description='CRUD operations for DynamoDB')

item_model = dynamo_ns.model('Item', {
    'cpf': fields.String(required=True, description='CPF do usuário'),
    'email': fields.String(required=True, description='Email do usuário'),
    'nome': fields.String(required=True, description='Nome do usuário')
})

def get_dynamo_repository():
    return DynamoRepository(region_name=AWS_REGION, table_name=DYNAMO_TABLE_NAME)

@dynamo_ns.route('/create')
class CreateResource(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.dynamo_repository = kwargs.get('dynamo_repository', get_dynamo_repository())

    @dynamo_ns.expect(item_model)
    def post(self):
        data = dynamo_ns.payload
        validation = validate_document(data['cpf'])
        if not validation['status']:
            return {'message': INVALID_CPF}, 400
        result = self.dynamo_repository.create_item(data['cpf'], data['email'], data['nome'])
        if result:
            logger.info('Create resource')
            return {'message': 'Item created successfully'}, 201
        else:
            return {'message': 'Failed to create item'}, 500

@dynamo_ns.route('/read/<string:cpf>')
class ReadResource(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.dynamo_repository = kwargs.get('dynamo_repository', get_dynamo_repository())

    def get(self, cpf):
        validation = validate_document(cpf)
        if not validation['status']:
            return {'message': INVALID_CPF}, 400
        item = self.dynamo_repository.read_item(cpf)
        if item:
            logger.info('Read resource')
            return item, 200
        else:
            return {'message': 'Item not found'}, 404

@dynamo_ns.route('/update/<string:cpf>')
class UpdateResource(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.dynamo_repository = kwargs.get('dynamo_repository', get_dynamo_repository())

    @dynamo_ns.expect(item_model)
    def put(self, cpf):
        validation = validate_document(cpf)
        if not validation['status']:
            return {'message': INVALID_CPF}, 400
        data = dynamo_ns.payload
        result = self.dynamo_repository.update_item(cpf, email=data.get('email'), nome=data.get('nome'))
        if result:
            logger.info('Update resource')
            return {'message': 'Item updated successfully'}, 200
        else:
            return {'message': 'Failed to update item'}, 500

@dynamo_ns.route('/delete/<string:cpf>')
class DeleteResource(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.dynamo_repository = kwargs.get('dynamo_repository', get_dynamo_repository())

    def delete(self, cpf):
        validation = validate_document(cpf)
        if not validation['status']:
            return {'message': INVALID_CPF}, 400
        result = self.dynamo_repository.delete_item(cpf)
        if result:
            logger.info('Delete resource')
            return {'message': 'Item deleted successfully'}, 200
        else:
            return {'message': 'Failed to delete item'}, 500
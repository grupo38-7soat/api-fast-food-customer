import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restx import Api
from src.services.resources.api_resources import dynamo_ns, CreateResource, ReadResource, UpdateResource, DeleteResource

class TestApiResources(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.api = Api(cls.app)
        cls.api.add_namespace(dynamo_ns, path='/dynamo')
        cls.client = cls.app.test_client()

    @patch('src.services.resources.api_resources.Config.get')
    @patch('src.services.resources.api_resources.DynamoRepository', autospec=True)
    @patch('src.services.resources.api_resources.validate_document')
    def test_create_resource(self, mock_validate_document, mock_dynamo_repository, mock_config_get):
        mock_config_get.side_effect = lambda key: 'mock_value' if key in ['awsRegion', 'dynamoTableName'] else None
        mock_validate_document.return_value = {'status': True}
        mock_dynamo_instance = mock_dynamo_repository.return_value
        mock_dynamo_instance.create_item.return_value = True

        response = self.client.post('/dynamo/create', json={
            'cpf': '12345678900',
            'email': 'test@example.com',
            'nome': 'Test User'
        })

        print(response.status_code)  # Add logging to see the actual status code
        print(response.json)  # Add logging to see the actual response

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'message': 'Item created successfully'})

    @patch('src.services.resources.api_resources.Config.get')
    @patch('src.services.resources.api_resources.DynamoRepository', autospec=True)
    @patch('src.services.resources.api_resources.validate_document')
    def test_read_resource(self, mock_validate_document, mock_dynamo_repository, mock_config_get):
        mock_config_get.side_effect = lambda key: 'mock_value' if key in ['awsRegion', 'dynamoTableName'] else None
        mock_validate_document.return_value = {'status': True}
        mock_dynamo_instance = mock_dynamo_repository.return_value
        mock_dynamo_instance.read_item.return_value = {
            'cpf': '12345678900',
            'email': 'test@example.com',
            'nome': 'Test User'
        }

        response = self.client.get('/dynamo/read/12345678900')

        print(response.status_code)  # Add logging to see the actual status code
        print(response.json)  # Add logging to see the actual response

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'cpf': '12345678900',
            'email': 'test@example.com',
            'nome': 'Test User'
        })

    @patch('src.services.resources.api_resources.Config.get')
    @patch('src.services.resources.api_resources.DynamoRepository', autospec=True)
    @patch('src.services.resources.api_resources.validate_document')
    def test_update_resource(self, mock_validate_document, mock_dynamo_repository, mock_config_get):
        mock_config_get.side_effect = lambda key: 'mock_value' if key in ['awsRegion', 'dynamoTableName'] else None
        mock_validate_document.return_value = {'status': True}
        mock_dynamo_instance = mock_dynamo_repository.return_value
        mock_dynamo_instance.update_item.return_value = True

        response = self.client.put('/dynamo/update/12345678900', json={
            'email': 'new@example.com',
            'nome': 'New Name'
        })

        print(response.status_code)  # Add logging to see the actual status code
        print(response.json)  # Add logging to see the actual response

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Item updated successfully'})

    @patch('src.services.resources.api_resources.Config.get')
    @patch('src.services.resources.api_resources.DynamoRepository', autospec=True)
    @patch('src.services.resources.api_resources.validate_document')
    def test_delete_resource(self, mock_validate_document, mock_dynamo_repository, mock_config_get):
        mock_config_get.side_effect = lambda key: 'mock_value' if key in ['awsRegion', 'dynamoTableName'] else None
        mock_validate_document.return_value = {'status': True}
        mock_dynamo_instance = mock_dynamo_repository.return_value
        mock_dynamo_instance.delete_item.return_value = True

        response = self.client.delete('/dynamo/delete/12345678900')

        print(response.status_code)  # Add logging to see the actual status code
        print(response.json)  # Add logging to see the actual response

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Item deleted successfully'})

if __name__ == '__main__':
    unittest.main()
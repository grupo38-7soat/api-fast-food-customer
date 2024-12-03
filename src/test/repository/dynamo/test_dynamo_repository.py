import pytest
from moto import mock_aws
import boto3
from repository.dynamo_db.dynamo_repository import DynamoRepository

@pytest.fixture
def dynamo_table():
    # Mock o DynamoDB
    with mock_aws():
        # Cria o recurso DynamoDB
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

        # Cria uma tabela mock para o teste
        table = dynamodb.create_table(
            TableName='TestTable',
            KeySchema=[
                {'AttributeName': 'cpf', 'KeyType': 'HASH'}  # Chave de partição
            ],
            AttributeDefinitions=[
                {'AttributeName': 'cpf', 'AttributeType': 'S'}  # Tipo de dado (String)
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # Espera até que a tabela esteja disponível
        table.meta.client.get_waiter('table_exists').wait(TableName='TestTable')

        yield table

@pytest.fixture
def dynamo_repository(dynamo_table):
    # Retorna uma instância da classe para teste
    return DynamoRepository(region_name='us-east-1', table_name='TestTable')

def test_create_item(dynamo_repository):
    result = dynamo_repository.create_item(cpf="12345678901", email="test@example.com", nome="Test User")
    assert result is True

def test_read_item(dynamo_repository):
    dynamo_repository.create_item(cpf="12345678901", email="test@example.com", nome="Test User")
    item = dynamo_repository.read_item(cpf="12345678901")
    assert item['cpf'] == "12345678901"
    assert item['email'] == "test@example.com"
    assert item['nome'] == "Test User"

def test_update_item(dynamo_repository):
    dynamo_repository.create_item(cpf="12345678901", email="test@example.com", nome="Test User")
    response = dynamo_repository.update_item(cpf="12345678901", email="newemail@example.com")
    assert response['Attributes']['email'] == "newemail@example.com"

def test_delete_item(dynamo_repository):
    dynamo_repository.create_item(cpf="12345678901", email="test@example.com", nome="Test User")
    result = dynamo_repository.delete_item(cpf="12345678901")
    assert result is True
    item = dynamo_repository.read_item(cpf="12345678901")
    assert item is None

import os
import boto3
from loguru import logger
from botocore.exceptions import ClientError


class DynamoRepository:
    def __init__(self, region_name=None, table_name=None):
        self.region_name = region_name
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb',
                                       region_name=self.region_name,
                                       aws_access_key_id=os.getenv('ACCESS_KEY'),
                                       aws_secret_access_key=os.getenv('SECRET_KEY')
                                       )
        self.table = self.dynamodb.Table(self.table_name)

    def create_item(self, cpf, email, nome):
        item = {
            'cpf': cpf,
            'email': email,
            'nome': nome
        }
        try:
            self.table.put_item(Item=item)
            logger.info(f"Item created: {item}")
            return True
        except ClientError as e:
            logger.exception(f"Error creating item: {e.response['Error']['Message']}")
            return False

    def read_item(self, cpf):
        try:
            response = self.table.get_item(Key={'cpf': cpf})
            logger.info(f"Item read: {response.get('Item', None)}")
            return response.get('Item', None)
        except ClientError as e:
            logger.exception(f"Error reading item: {e.response['Error']['Message']}")
            return None

    def update_item(self, cpf, email=None, nome=None):
        update_expression = []
        expression_attribute_values = {}

        if email:
            update_expression.append('email = :email')
            expression_attribute_values[':email'] = email
        if nome:
            update_expression.append('nome = :nome')
            expression_attribute_values[':nome'] = nome

        if not update_expression:
            logger.exception("No attributes to update")
            return None

        update_expression = 'SET ' + ', '.join(update_expression)

        try:
            response = self.table.update_item(
                Key={'cpf': cpf},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW"
            )

            logger.info(f"Item updated: {response.get('Attributes', None)}")
            return response
        except ClientError as e:
            logger.exception(f"Error updating item: {e.response['Error']['Message']}")
            return None

    def delete_item(self, cpf):
        try:
            self.table.delete_item(Key={'cpf': cpf})
            logger.info(f"Item deleted: {cpf}")
            return True
        except ClientError as e:
            logger.exception(f"Error deleting item: {e.response['Error']['Message']}")
            return False

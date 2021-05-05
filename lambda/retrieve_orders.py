import json
import boto3
import os

ddb = boto3.resource('dynamodb')
orders_table = ddb.Table(os.getenv('ORDERS_TABLE_NAME'))


def handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(orders_table.scan())
    }



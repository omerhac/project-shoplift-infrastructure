from aws_cdk import core
import aws_cdk.aws_lambda as _lambda
from aws_cdk.aws_apigateway import LambdaRestApi
from aws_cdk.aws_dynamodb import Table, AttributeType


class OrderRetriever(core.Construct):
    """Construct for order retrieval API of project Shoplift"""
    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        retrieve_orders_lambda = _lambda.Function(self, 'ShopliftRetrieveOrder',
                                                  code=_lambda.Code.asset('lambda'),
                                                  handler='retrieve_orders.handler',
                                                  runtime=_lambda.Runtime.PYTHON_3_8,
                                                  environment={
                                                      'ORDERS_TABLE_NAME': 'ShopliftOrdersTable'
                                                  })

        retrieve_order_api = LambdaRestApi(self, 'ShopliftRetrieveOrderAPI',
                                           handler=retrieve_orders_lambda)

        orders_table = Table(self, 'ShopliftOrdersTable',
                             table_name='ShopliftOrdersTable',
                             partition_key={
                                 'name': 'order_id', 'type': AttributeType.STRING
                             })

        orders_table.grant_read_data(retrieve_orders_lambda)  # grant lambda permissions to read from ddb

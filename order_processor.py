from aws_cdk import core
import aws_cdk.aws_lambda as _lambda
from aws_cdk.aws_apigateway import LambdaRestApi


class OrderProcessor(core.Construct):
    """Construct for order processing logic of project Shoplift"""
    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        process_order_lambda = _lambda.Function(self, 'ShopliftProcessOrder',
                                                code=_lambda.Code.asset('lambda'),
                                                handler='lambda_handler.handler',
                                                runtime=_lambda.Runtime.PYTHON_3_8)

        process_order_api = LambdaRestApi(self, 'ShopliftProcessOrderAPI',
                                          handler=process_order_lambda)
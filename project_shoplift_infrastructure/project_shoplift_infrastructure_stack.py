from aws_cdk import core as cdk
from aws_cdk.aws_ec2 import Vpc
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService, ApplicationLoadBalancedTaskImageOptions
from aws_cdk.aws_ecs import ContainerImage, Cluster
from aws_cdk.aws_apigateway import LambdaRestApi
import aws_cdk.aws_lambda as _lambda
from aws_cdk.aws_ecr import Repository
from aws_cdk.aws_dynamodb import Table, AttributeType
from aws_cdk import core


class ProjectShopliftInfrastructureStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # setting up voice recognition fargate service
        shoplift_cluster = Cluster(self, 'ShopliftCluster', cluster_name='ShopliftCluster')
        apache_rep = Repository.from_repository_name(self, 'ApacheFlaskRep', repository_name='apache-flask')
        voice_recognition_image = ContainerImage.from_ecr_repository(repository=apache_rep,
                                                                     tag='latest')
        voice_recognition_task = ApplicationLoadBalancedTaskImageOptions(image=voice_recognition_image,
                                                                         container_port=80)
        loadbalanced_fargate_service = ApplicationLoadBalancedFargateService(self, 'ShopliftVoiceRecognitionService',
                                                                             cpu=256,
                                                                             memory_limit_mib=1024,
                                                                             task_image_options=voice_recognition_task,
                                                                             cluster=shoplift_cluster,
                                                                             desired_count=4,
                                                                             listener_port=80,
                                                                             public_load_balancer=True)

        # setting up order processing lambda-api
        process_order_lambda = _lambda.Function(self, 'ShopliftProcessOrder',
                                                code=_lambda.Code.asset('lambda'),
                                                handler='lambda_handler.handler',
                                                runtime=_lambda.Runtime.PYTHON_3_8)
        process_order_api = LambdaRestApi(self, 'ShopliftProcessOrderAPI',
                                          handler=process_order_lambda)

        # setting up users orders retrieval api
        retrieve_orders_lambda = _lambda.Function(self, 'ShopliftRetrieveOrder',
                                                  code=_lambda.Code.asset('lambda'),
                                                  handler='lambda_handler.handler',
                                                  runtime=_lambda.Runtime.PYTHON_3_8)
        retrive_order_api = LambdaRestApi(self, 'ShopliftRetrieveOrderAPI',
                                          handler=retrieve_orders_lambda)
        orders_table = Table(self, 'ShopliftOrdersTable',
                             table_name='SopliftOrdersTable',
                             partition_key={
                                 'name': 'order_id', 'type': AttributeType.STRING
                             })

from aws_cdk import core as cdk
from aws_cdk.aws_ec2 import Vpc
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService, ApplicationLoadBalancedTaskImageOptions
from aws_cdk.aws_ecs import ContainerImage, Cluster
from aws_cdk.aws_apigateway import LambdaRestApi
import aws_cdk.aws_lambda as _lambda

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class ProjectShopliftInfrastructureStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # setting up voice recognition fargate service
        shoplift_cluster = Cluster(self, 'ShopliftCluster', cluster_name='ShopliftCluster')
        voice_recognition_task = ApplicationLoadBalancedTaskImageOptions(image=ContainerImage.from_registry('tutum/hello-world:latest'),
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

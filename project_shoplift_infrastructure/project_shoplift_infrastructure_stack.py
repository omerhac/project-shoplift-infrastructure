from aws_cdk import core as cdk
from aws_cdk.aws_ec2 import Vpc

import voice_recognition, order_processor, order_retriever


class ProjectShopliftInfrastructureStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = Vpc(self, 'VPC', max_azs=3)

        # setting up voice recognition fargate service
        voice_recognition_service = voice_recognition.VoiceRecognitionService(self, 'ShopliftVoiceRecognition', vpc=vpc)

        # setting up order processing lambda-api
        process_order_api = order_processor.OrderProcessor(self, 'ShopliftProcessOrderAPI')

        # setting up users orders retrieval api
        retrive_orders_api = order_retriever.OrderRetriever(self, 'ShopliftRetriveOrdersAPI')

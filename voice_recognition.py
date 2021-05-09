from aws_cdk import core
from aws_cdk.aws_ecs import Cluster, ContainerImage
from aws_cdk.aws_ecr import Repository
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService, ApplicationLoadBalancedTaskImageOptions


class VoiceRecognitionService(core.Construct):
    """Construct for the speech to text service of project Shoplift"""

    def __init__(self, scope, construct_id, vpc, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        shoplift_cluster = Cluster(self, 'ShopliftCluster', cluster_name='ShopliftCluster', vpc=vpc)
        apache_rep = Repository.from_repository_name(self, 'ApacheFlaskRep',
                                                     repository_name='apache-flask')

        voice_recognition_image = ContainerImage.from_ecr_repository(repository=apache_rep,
                                                                     tag='latest')

        voice_recognition_task = ApplicationLoadBalancedTaskImageOptions(image=voice_recognition_image,
                                                                         container_port=80)

        loadbalanced_fargate_service = ApplicationLoadBalancedFargateService(self, 'ShopliftVoiceRecognitionService',
                                                                             cpu=256,
                                                                             memory_limit_mib=1024,
                                                                             task_image_options=voice_recognition_task,
                                                                             cluster=shoplift_cluster,
                                                                             desired_count=1,
                                                                             listener_port=80
                                                                             )

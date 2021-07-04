from aws_cdk import (aws_iam as iam, core)

from .constructs import YOLOv3Service


class ServerlessStack(core.Stack):
    """Provision Lambda and API Gateway.
    """
    def __init__(self, scope: core.Construct, construct_id: str,
                 **kwargs) -> None:

        super().__init__(scope, construct_id, **kwargs)

        YOLOv3Service(self, "YOLOv3")

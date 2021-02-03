from aws_cdk import core

from .constructs import MLEfs, MLVpc


class MachineLearningStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        vpc_construct = MLVpc(self, "ml-vpc")

        # Create EFS
        efs_stack = MLEfs(
            self,
            "ml-efs",
            vpc=vpc_construct.vpc
        )

        # Install machine learning libraries


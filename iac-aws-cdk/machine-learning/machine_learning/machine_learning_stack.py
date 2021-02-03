from aws_cdk import core

from .constructs import MLEfs, MLLib, MLVpc


class MachineLearningStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        vpc_construct = MLVpc(self, "ml-vpc")

        # Create EFS
        efs_construct = MLEfs(
            self,
            "ml-efs",
            vpc=vpc_construct.vpc
        )

        # Install machine learning libraries
        lib_construct = MLLib(
            self,
            "ml-lib",
            vpc=vpc_construct.vpc,
            ec2_instance_type="t2.micro",
            efs_share=efs_construct.efs_share,
            efs_sg=efs_construct.efs_sg
        )

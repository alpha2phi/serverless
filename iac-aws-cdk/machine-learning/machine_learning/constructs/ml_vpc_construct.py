import os.path

from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from aws_cdk import core
from aws_cdk.aws_s3_assets import Asset

dirname = os.path.dirname(__file__)

class MLVpc(core.Construct):

    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

import os.path

from aws_cdk import aws_ec2 as ec2
from aws_cdk import core
from aws_cdk.aws_s3_assets import Asset


class MLVpc(core.Construct):
    """Build a VPC."""

    def __init__(self, scope: core.Construct, id: str, vpc_name: str = None,  **kwargs):
        super().__init__(scope, id, **kwargs)

        if vpc_name is not None:
            self.vpc = ec2.Vpc.from_lookup(
                self, "vpc",
                vpc_name=vpc_name
            )
        else:
            self.vpc = ec2.Vpc(
                self,
                "alpha2phi_ml_vpc",
                cidr="10.20.0.0/16",
                max_azs=1,
                nat_gateways=1,
                enable_dns_support=True,
                enable_dns_hostnames=True,
                subnet_configuration=[
                    ec2.SubnetConfiguration(
                        name="public", cidr_mask=24, subnet_type=ec2.SubnetType.PUBLIC
                    ),
                    ec2.SubnetConfiguration(
                        name="private", cidr_mask=24, subnet_type=ec2.SubnetType.PRIVATE
                    ),
                    ec2.SubnetConfiguration(
                        name="isolated", cidr_mask=24, subnet_type=ec2.SubnetType.ISOLATED
                    )
                ]
            )

        output_1 = core.CfnOutput(
            self,
            "VpcId",
            value=self.vpc.vpc_id,
            export_name="VpcId"
        )

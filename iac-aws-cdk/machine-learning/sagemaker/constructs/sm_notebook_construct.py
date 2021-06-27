from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam_
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_sagemaker as sm
from aws_cdk import core


class SageMakerNotebookStruct(core.Construct):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        self.vpc = ec2.Vpc(self, "VPC",
                           max_azs=2,
                           cidr="10.10.0.0/16",
                           subnet_configuration=[ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               name="Public",
                               cidr_mask=24
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE,
                               name="Private",
                               cidr_mask=24
                           )
                           ],
                           nat_gateways=1
                           )

        # Security group
        # self.sg = ec2.SecurityGroup(self, "securityGroup", self.vpc)
        self.sg = ec2.SecurityGroup.from_security_group_id(
            self, "securityGroup", self.vpc.vpc_default_security_group, mutable=False)

        # Create S3 bucket
        self.bucket = s3.Bucket(
            self, "alpha2phi_sm_notebook_s3_bucket", removal_policy=core.RemovalPolicy.DESTROY)

        # IAM Roles
        # Create role for Notebook instance
        nRole = iam_.Role(
            self,
            "notebookAccessRole",
            assumed_by=iam_.ServicePrincipal('sagemaker'))

        nPolicy = iam_.Policy(
            self,
            "notebookAccessPolicy",
            policy_name="notebookAccessPolicy",
            statements=[iam_.PolicyStatement(actions=['s3:*', 'sagemaker:*'], resources=['*', ]), ]).attach_to_role(nRole)

        # Create notebook instances cluster
        nid = 'CDK-Notebook-Instance-ML-1'
        notebook = sm.CfnNotebookInstance(
            self,
            nid,
            instance_type='ml.t2.medium',
            volume_size_in_gb=5,
            security_group_ids=[self.sg.security_group_id],
            subnet_id=self.vpc.private_subnets[0].subnet_id,
            notebook_instance_name=nid,
            role_arn=nRole.role_arn
        )

        core.CfnOutput(self, "VPC Id", value=self.vpc.vpc_id)
        core.CfnOutput(self, "Bucket", value=self.bucket.bucket_arn)
        core.CfnOutput(self, "Notebook instance name",
                       value=notebook.notebook_instance_name)

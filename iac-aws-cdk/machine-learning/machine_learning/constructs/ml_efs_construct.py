from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_efs as efs
from aws_cdk import core


class MLEfs(core.Construct):
    """Build a EFS."""

    def __init__(self,
                 scope: core.Construct,
                 id: str,
                 vpc,
                 efs_mnt_path: str = "/machine_learning",
                 **kwargs
                 ) -> None:

        super().__init__(scope, id, **kwargs)

        # Create Security Group to connect to EFS
        self.efs_sg = ec2.SecurityGroup(
            self,
            id="efsSecurityGroup",
            vpc=vpc,
            security_group_name=f"efs_sg_{id}",
            description="Security Group to connect to EFS from the VPC"
        )

        self.efs_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(2049),
            description="Allow EC2 instances within the same VPC to connect to EFS"
        )

        # Create the EFS filesystem
        self.efs_share = efs.FileSystem(
            self,
            "elasticFileSystem",
            file_system_name=f"high-performance-storage",
            vpc=vpc,
            security_group=self.efs_sg,
            encrypted=False,
            lifecycle_policy=efs.LifecyclePolicy.AFTER_7_DAYS,
            performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,
            throughput_mode=efs.ThroughputMode.BURSTING,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Create EFS ACL
        efs_acl = efs.Acl(
            owner_gid="1000",
            owner_uid="1000",
            permissions="0750"
        )

        # Create EFS POSIX user
        efs_user = efs.PosixUser(
            gid="1000",
            uid="1000"
        )

        # Create EFS access point
        self.efs_ap = efs.AccessPoint(
            self,
            "efsDefaultAccessPoint",
            path=f"{efs_mnt_path}",
            file_system=self.efs_share,
            posix_user=efs_user,
            create_acl=efs_acl
        )

        output_0 = core.CfnOutput(
            self,
            "MountEfs",
            value=f"sudo mount -t efs -o tls {self.efs_share.file_system_id}:/ /mnt{efs_mnt_path}",
            description=f"Use this command to mount efs using efs helper utility at location /mnt{efs_mnt_path}"
        )

from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from aws_cdk import core


class MLLib(core.Construct):
    """Install machine learning libraries."""

    def __init__(
            self,
            scope: core.Construct,
            id: str,
            vpc,
            ec2_instance_type: str,
            efs_share,
            efs_sg,
            **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # User data
        user_data_part_01 = ("""#!/bin/bash
                        set -ex
                        EFS_MNT="/machine_learning"
                        ML_LIB_HOME="${EFS_MNT}"
                        EFS_USER_ID=1000
                        sudo yum -y install python3
                        sudo yum -y install amazon-efs-utils
                        sudo mkdir -p ${EFS_MNT}
                        """
                             )

        user_data_part_02 = f"sudo mount -t efs -o tls {efs_share.file_system_id}:/ /machine_learning"
        user_data_part_03 = ("""
                        sudo mkdir -p ${ML_LIB_HOME}
                        cd ${ML_LIB_HOME}
                        sudo pip3 install --no-cache-dir -U -t ${ML_LIB_HOME}/libs https://download.pytorch.org/whl/cpu/torch-1.7.1%2Bcpu-cp37-cp37m-linux_x86_64.whl
                        sudo pip3 install --no-cache-dir -U -t ${ML_LIB_HOME}/libs https://download.pytorch.org/whl/cpu/torchvision-0.8.2%2Bcpu-cp37-cp37m-linux_x86_64.whl
                        sudo chown -R ${EFS_USER_ID}:${EFS_USER_ID} ${ML_LIB_HOME}
                        """
                             )

        user_data = user_data_part_01 + user_data_part_02 + user_data_part_03

        # Get the latest AMI from AWS SSM
        linux_ami = ec2.AmazonLinuxImage(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2)

        # Get the latest AMI
        amzn_linux_ami = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2)

        # EC2 Instance Role
        instance_role = iam.Role(
            self, "ml-lib-instance-role",
            assumed_by=iam.ServicePrincipal(
                "ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonSSMManagedInstanceCore"
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AWSXRayDaemonWriteAccess"
                )
            ]
        )

        # EC2 instance
        self.ec2_instance = ec2.Instance(
            self,
            "mllib-ec2-instance",
            instance_type=ec2.InstanceType(
                instance_type_identifier=f"{ec2_instance_type}"),
            instance_name="mllib-ec2-instance",
            machine_image=amzn_linux_ami,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/xvda",
                    volume=ec2.BlockDeviceVolume.ebs(
                        volume_size=10
                    )
                )
            ],
            role=instance_role,
            user_data=ec2.UserData.custom(
                user_data)
        )

        self.ec2_instance.add_security_group(efs_sg)

        # Outputs
        output_0 = core.CfnOutput(
            self,
            "ec2-instance-ip",
            value=f"http://{self.ec2_instance.instance_private_ip}",
            description=f"Private IP address of the server"
        )

        output_1 = core.CfnOutput(
            self,
            "ec2-instance-login-url",
            value=(
                f"https://console.aws.amazon.com/ec2/v2/home?region="
                f"{core.Aws.REGION}"
                f"#Instances:search="
                f"{self.ec2_instance.instance_id}"
                f";sort=instanceId"
            ),
            description=f"Login to the instance using Systems Manager"
        )

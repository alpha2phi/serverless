from aws_cdk import core

from .constructs import S3Bucket, S3Site


class BasicStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a S3 bucket
        s3_bucket = S3Bucket(
            self, "MyS3Bucket", bucket_id="alpha2phi_basic_s3_bucket"
        )

        # Create a static web site
        s3_site = S3Site(
            self, "MyS3Site", bucket_id="alpha2phi_basic_s3_site", deployment_id="apha2phi_basic_s3_site"
        )

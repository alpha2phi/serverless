from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as deployment
from aws_cdk import core


class S3Site(core.Construct):
    @property
    def bucket(self):
        return self._bucket

    def __init__(self, scope: core.Construct, id: str, bucket_id: str, deployment_id: str,  **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create a S3 bucket for static website
        self._bucket = s3.Bucket(self, bucket_id,
                                 public_read_access=True,
                                 website_index_document="index.html",
                                 removal_policy=core.RemovalPolicy.DESTROY)

        # Deploy the static website
        self._deployment = deployment.BucketDeployment(
            self, deployment_id, sources=[deployment.Source.asset("./website")], destination_bucket=self._bucket)

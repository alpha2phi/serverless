from aws_cdk import aws_s3 as s3
from aws_cdk import core


class S3Bucket(core.Construct):
    @property
    def bucket(self):
        return self._bucket    

    def __init__(self, scope: core.Construct, id: str, bucket_id:str,  **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create a S3 bucket. Setting removal policy so that "cdk destroy" will work
        self._bucket = s3.Bucket(self, bucket_id, removal_policy=core.RemovalPolicy.DESTROY)

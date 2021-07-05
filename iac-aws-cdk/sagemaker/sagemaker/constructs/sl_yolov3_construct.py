from aws_cdk import (core, aws_apigateway as apigateway, aws_s3 as s3,
                     aws_lambda as lambda_, aws_iam as iam)

# https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_apigateway/README.html
# https://docs.aws.amazon.com/cdk/latest/guide/serverless_example.html
# https://debugthis.dev/cdk/2020-30-06-aws-cdk-code-pipeline/


class YOLOv3Service(core.Construct):

    ENDPOINT_NAME = "yolo-v32021"

    def __init__(self, scope: core.Construct, id: str):
        super().__init__(scope, id)

        role = iam.Role(
            self,
            "YOLOv3Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"))
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaVPCAccessExecutionRole"))
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSageMakerFullAccess"))

        bucket = s3.Bucket(self, "YOLOv3Store")

        handler = lambda_.Function(self,
                                   "YOLOv3Handler",
                                   runtime=lambda_.Runtime.PYTHON_3_8,
                                   code=lambda_.Code.from_asset("resources"),
                                   handler="yolov3.lambda_handler",
                                   role=role,
                                   timeout=core.Duration.seconds(60),
                                   environment=dict(
                                       BUCKET=bucket.bucket_name,
                                       ENDPOINT_NAME=self.ENDPOINT_NAME))

        bucket.grant_read_write(handler)
        api = apigateway.LambdaRestApi(self,
                                       "yolov3-api",
                                       handler=handler,
                                       proxy=False)
        inference = api.root.add_resource("inference")
        inference.add_method(
            "POST", authorization_type=apigateway.AuthorizationType.NONE)

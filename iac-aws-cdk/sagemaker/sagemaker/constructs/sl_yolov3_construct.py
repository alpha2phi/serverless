from aws_cdk import (core, aws_apigateway as apigateway, aws_s3 as s3,
                     aws_lambda as lambda_, aws_iam as iam)


class YOLOv3Service(core.Construct):
    def __init__(self, scope: core.Construct, id: str):
        super().__init__(scope, id)

        role = iam.Role(
            self,
            "YOLOv3 Role",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"))
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"))
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaVPCAccessExecutionRole"))
        role.add_managed_policy(
            iam.ManagedPolicy.from_managed_policy_arn(
                self,
                "SageMakerRole",
                managed_policy_arn=
                "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"))

        bucket = s3.Bucket(self, "YOLOv3Store")

        handler = lambda_.Function(self,
                                   "YOLOv3Handler",
                                   runtime=lambda_.Runtime.PYTHON_3_8,
                                   code=lambda_.Code.from_asset("resources"),
                                   handler="yolov3.lambda_handler",
                                   environment=dict(BUCKET=bucket.bucket_name))

        bucket.grant_read_write(handler)

        api = apigateway.RestApi(self,
                                 "yolov3-api",
                                 rest_api_name="YOLOv3 Service",
                                 description="YOLOv3 Services")

        post_api = apigateway.LambdaIntegration(
            handler,
            request_templates={"application/json": '{ "statusCode": "200" }'})

        api.root.add_method("POST", post_api)

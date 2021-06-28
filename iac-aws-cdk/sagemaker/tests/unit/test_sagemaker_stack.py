import json
import pytest

from aws_cdk import core
from sagemaker.sagemaker_stack import SagemakerStack


def get_template():
    app = core.App()
    SagemakerStack(app, "sagemaker")
    return json.dumps(app.synth().get_stack("sagemaker").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())

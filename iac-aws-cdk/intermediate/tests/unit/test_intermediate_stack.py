import json
import pytest

from aws_cdk import core
from intermediate.intermediate_stack import IntermediateStack


def get_template():
    app = core.App()
    IntermediateStack(app, "intermediate")
    return json.dumps(app.synth().get_stack("intermediate").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())

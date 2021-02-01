import json
import pytest

from aws_cdk import core
from basic.basic_stack import BasicStack


def get_template():
    app = core.App()
    BasicStack(app, "basic")
    return json.dumps(app.synth().get_stack("basic").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())

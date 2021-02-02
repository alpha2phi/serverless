import json
import pytest

from aws_cdk import core
from machine-learning.machine_learning_stack import MachineLearningStack


def get_template():
    app = core.App()
    MachineLearningStack(app, "machine-learning")
    return json.dumps(app.synth().get_stack("machine-learning").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())

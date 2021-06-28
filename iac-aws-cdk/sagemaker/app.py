#!/usr/bin/env python3

from aws_cdk import core

from sagemaker.sagemaker_stack import SagemakerStack

app = core.App()
SagemakerStack(app, "sagemaker", env={'region': 'ap-southeast-1'})

app.synth()

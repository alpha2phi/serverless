#!/usr/bin/env python3

from aws_cdk import core

from sagemaker.serverless_stack import ServerlessStack

app = core.App()

ServerlessStack(app, "serverless", env={'region': 'ap-southeast-1'})

app.synth()

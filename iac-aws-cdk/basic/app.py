#!/usr/bin/env python3

from aws_cdk import core

from basic.basic_stack import BasicStack


app = core.App()
BasicStack(app, "basic", env={'region': 'us-west-2'})

app.synth()

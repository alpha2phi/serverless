#!/usr/bin/env python3

from aws_cdk import core

from intermediate.intermediate_stack import IntermediateStack


app = core.App()
IntermediateStack(app, "intermediate", env={'region': 'us-west-2'})

app.synth()

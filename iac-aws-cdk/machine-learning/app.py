#!/usr/bin/env python3

from aws_cdk import core

from machine_learning.machine_learning_stack import MachineLearningStack


app = core.App()
MachineLearningStack(app, "machine-learning", env={'region': 'us-west-2'})

app.synth()

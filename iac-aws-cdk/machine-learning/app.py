#!/usr/bin/env python3

from aws_cdk import core

from machine_learning.machine_learning_stack import MachineLearningStack
from sagemaker.sagemaker_stack import SageMakerStack

app = core.App()

# Install ML libraries
# MachineLearningStack(app, "machine-learning", env={'region': 'ap-southeast-1'})

# Create SageMaker notebook
SageMakerStack(app, "sagemaker-ml-stack", env={'region': 'ap-southeast-1'})

app.synth()

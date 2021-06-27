from aws_cdk import core

from .constructs import SageMakerNotebookStruct


class SageMakerStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create SageMaker notebook
        sm_notebook_construct = SageMakerNotebookStruct(self, "ml-vpc")

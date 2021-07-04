from aws_cdk import (aws_iam as iam, core)

from .constructs import widget_service


class WidgetServiceStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        WidgetService(self, "Widgets")

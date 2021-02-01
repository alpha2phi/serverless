from aws_cdk import (
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    core
)


class IntermediateStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self, "IntermediateQueue",
            visibility_timeout=core.Duration.seconds(300),
        )

        topic = sns.Topic(
            self, "IntermediateTopic"
        )

        topic.add_subscription(subs.SqsSubscription(queue))

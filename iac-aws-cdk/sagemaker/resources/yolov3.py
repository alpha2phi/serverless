import os
import boto3
import json
import base64

ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime = boto3.client('runtime.sagemaker')


def lambda_handler(event, context):
    data = json.loads(event['body'])
    payload = data['data']
    print(payload)
    print(f"End point={ENDPOINT_NAME}")
    payload = base64.b64decode(payload)

    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='image/jpeg',
                                       Accept='image/jpeg',
                                       Body=payload)
    print(response)
    result = json.loads(response['Body'].read().decode())
    print(result)
    body = json.dumps({"result": json.dumps(result)})

    return {
        "statusCode": 200,
        "headers": {},
        "body": body,
        "isBase64Encoded": False
    }

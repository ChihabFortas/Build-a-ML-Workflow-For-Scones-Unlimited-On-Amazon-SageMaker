import os
import io
import boto3
import json
import base64

# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2023-01-18-19-42-56-366'

# https://boto3.amazonaws.com/v1/documentation/api/1.9.42/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client.invoke_endpoint
runtime= boto3.client('sagemaker-runtime')

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event["body"]["image_data"])

    # Instantiate a Predictor
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT,
        Body=image,
        ContentType='image/png'
    )
    
    decode_response = response['Body'].read().decode('utf-8')
    inferences = [float(x) for x in decode_response[1:-1].split(',')]

    return {
        'statusCode': 200,
        'inferences': inferences
    }
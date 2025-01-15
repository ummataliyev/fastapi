"""
AWS connection
"""
import boto3

from libs.environs import env


aws_client = boto3.client(
    "s3",
    aws_access_key_id=env.str("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=env.str("AWS_SECRET_ACCESS_KEY"),
    region_name=env.str("AWS_REGION_NAME"),
)

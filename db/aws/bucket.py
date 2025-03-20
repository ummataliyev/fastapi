"""
AWS connection
"""
import boto3

from libs.environs import env

AWS_IS_ENABLED = env.bool("AWS_IS_ENABLE", default=False)


if AWS_IS_ENABLED:
    aws_client = boto3.client(
        "s3",
        region_name=env.str("AWS_REGION_NAME"),
        aws_access_key_id=env.str("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=env.str("AWS_SECRET_ACCESS_KEY")
    )

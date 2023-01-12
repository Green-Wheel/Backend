import base64
import logging
import boto3
from botocore.exceptions import ClientError
import os


def get_session():
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    access_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    session = boto3.session.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=access_secret_key
    )
    return session


def upload_image_to_s3(file, path):
    session = get_session()
    s3 = session.resource('s3')
    bucket_name = os.getenv('BUCKET_NAME')
    # Upload the file
    try:
        s3.Bucket(bucket_name).put_object(Key=path, Body=file, ContentType=file.content_type, ACL='public-read')
        s3_path = "https://" + bucket_name + ".s3.eu-west-1.amazonaws.com/" + path
        return s3_path
    except ClientError as e:
        logging.error(e)
        return False

import logging
import boto3
from botocore.exceptions import ClientError
import os

def upload_image_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    access_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    session = boto3.session.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=access_secret_key
    )
    s3 = session.resource('s3')

    # Upload the file
    #s3_client = boto3.client('s3')
    try:
        object = s3.Object(bucket, object_name)
        result = object.put(Body=file_name)
        #response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_image_from_s3():
    s3 = boto3.client('s3')
    s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')

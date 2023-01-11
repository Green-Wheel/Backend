import base64
import logging
import boto3
from botocore.exceptions import ClientError
import os


def get_session():
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    access_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    print("access_key")
    print(access_key)
    print("access_secret")
    print(access_secret_key)
    session = boto3.session.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=access_secret_key
    )
    return session


def upload_image_to_s3(file, path):
    session = get_session()
    print("session")
    print(session)
    s3 = session.resource('s3')
    bucket_name = os.getenv('BUCKET_NAME')
    print("bucket_name", bucket_name)
    # Upload the file
    try:
        s3.Bucket(bucket_name).put_object(Key=path, Body=file, ContentType=file.content_type, ACL='public-read')
        s3_path = "https://" + bucket_name + ".s3.eu-west-1.amazonaws.com/" + path
        print("s3_path", s3_path)
        return s3_path
    except ClientError as e:
        logging.error(e)
        return False


def get_image_from_s3(path):
    session = get_session()
    s3 = session.resource('s3')

    obj = s3.Object('greenwheel-bucket', path)
    obj_serializable = base64.b64encode(obj.get()['Body'].read())
    return obj_serializable
    # try:
    #     file_stream = obj.get()['Body'].read()
    #     print(file_stream)
    #     return file_stream
    # except ClientError as e:
    #     logging.error(e)
    #     return False

#https://greenwheel-bucket.s3.eu-west-1.amazonaws.com/publication/1/foto.png?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHIaCWV1LXdlc3QtMyJIMEYCIQCf%2FeexkzTuWfKqQimc%2Blvs71UylhZb0SJvL8GNXnYvpgIhAPac1Huj1mQsT%2FV%2B2yblsZJKPURBvhZ3QYy%2B4qmoKCM%2BKuQCCHsQABoMMDA3MzcwNjUyMzg0IgwdADMq%2BMq%2FKs2F4psqwQJkNGg6zEo774cpYxmM6FPDzlSDRAsW6CC72%2F06iPKAQ0ybx0c%2B4AWJTA1%2FmPlRqzlo9saGkxmsjf1VPG0PFRPtlxhbjtQH9ntzpfXYiFMa9wo7MjLkAJ9FglsPO%2BdYIfowtW12VY%2F5nWvzySOhY3Aub9DFrGmlGsbCTuHSymuRrKkf9tSsKTqZWDU8C1wCALQhRjM5BA1Tqf34XA2E7%2BuVyFx9iCI6NrplnubBefpn9ni2jr%2BG0LRCIPE%2BSGf1E3ZODXGCLQ9i83NY7i9yXnaTShkAuqKSord8f8DAXiZ28NsvEgoGAOo8t%2BciD4tLQ%2FUIbXQzji2H6I1WXTvufvvHZhshR4OUTQTCfEq9%2B8eHADW43T%2B2r1lKXLG3AeVIoZa92mrXWge6QtW0Pe4TuxRYp7W2FqZOrKuTtMpUUA7JGEww0KHpmwY6sgL9gvYeblcNOc8LjRMXXU4Hma9Aw6zxy31QlvBIn3lChPiJJz5lDj9xAUONQ1d5Nyp7mAq74EV77wk4p2Dw2AKdIO9E0C9U7uW285WGbzdGJbKphQm3UtDafIyF8O4hkrjQ5dsrZjhbxLQbw%2BjBvw3NDqUh8hH4l8uvw%2FRwepMnjjTrLfMtwZc1bPUSpBpbrNm1dplEmmYkEXewMpm7D4yxvdI%2BBo2UijE14Wc5yMCI0itqTnA5bJs8wtEI8IInpbBdUjICn6vEJ8NGdzK6eAgXTubs3WvEUQAI1LfqkBL9ska9qeQiYxUhBEeXsPEh%2FvEzKea9zl3cqmnMaygm8%2B%2FsOGGjYZOxy%2BnIUFK%2BYAb6uwu9FTNJsoXfkT5XXhqKMhCTGTByGao%2Fuwn3wkAXTH3Nxng%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20221120T194757Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQDN2THLQJAFC26O2%2F20221120%2Feu-west-1%2Fs3%2Faws4_request&X-Amz-Signature=84331f7beb5e95c85ed0e3c2fd66eaf84f2e87847cd6ca03964d315b29ad1dbe
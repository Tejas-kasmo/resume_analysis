import boto3
import configparser
import re
import pandas as pd

def connect():

    config = configparser.ConfigParser()
    config.read(r'C:\Users\mysur\OneDrive\Desktop\python_tutorial\venv1\config.config')

    aws_access_key_id = config['AWS']['aws_access_key_id']
    aws_secret_access_key = config['AWS']['aws_secret_access_key']
    region_name = config['AWS']['region']

    s3 = boto3.client(
        's3',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    source_bucket = 'extracted-text-data-resume'

    response = s3.list_objects_v2(Bucket=source_bucket)

    return response, s3

import boto3
import PyPDF2
import configparser
from io import BytesIO

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

source_bucket = 'raw-resume-pdf-data'
text_bucket = 'extracted-text-data-resume'
archive_bucket = 'resume-data-archive'

response = s3.list_objects_v2(Bucket=source_bucket)

if 'Contents' in response:
    for obj in response['Contents']:
        file_key = obj['Key']

        if not file_key.lower().endswith('.pdf'):
            continue

        print(f"Processing file: {file_key}")

        file_obj = s3.get_object(Bucket=source_bucket, Key=file_key)
        pdf_content = file_obj['Body'].read()

        pdf_file = BytesIO(pdf_content)
        reader = PyPDF2.PdfReader(pdf_file)

        text = ''
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        txt_key = file_key.replace('.pdf', '.txt')
        s3.put_object(Bucket=text_bucket, Key=txt_key, Body=text.encode('utf-8'))

        print(f"Uploaded extracted text to {text_bucket}/{txt_key}")

        copy_source = {'Bucket': source_bucket, 'Key': file_key}
        s3.copy_object(CopySource=copy_source, Bucket=archive_bucket, Key=file_key)
        s3.delete_object(Bucket=source_bucket, Key=file_key)

        print(f"Moved PDF to {archive_bucket}/{file_key}")
        print("===================================================================================")

else:
    print("No files found in the bucket.")

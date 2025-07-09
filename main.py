import extract_from_S3
import transform_resume
import load_to_sql_server

responses, s3 = extract_from_S3.connect()

if 'Contents' in responses:
    for obj in responses['Contents']:
        file_key = obj['Key']
        
        name, email, phone, skills, linkedin, github = transform_resume.get_structured_data(file_key=file_key, s3=s3)
        load_to_sql_server.connect(name, email, phone, skills, linkedin, github)
        

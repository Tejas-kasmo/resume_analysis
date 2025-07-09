import PyPDF2
from io import BytesIO
import pandas as pd
import re

def get_structured_data(file_key, s3):

    file_obj = s3.get_object(Bucket="extracted-text-data-resume", Key=file_key)
    text = file_obj['Body'].read().decode('utf-8')

    lines = []
    for line in text.strip().split('\n'):
        stripped_line = line.strip()
        if stripped_line and not any(char.isdigit() for char in stripped_line):
            lines.append(stripped_line)

    if lines:
        name = lines[0]
    else:
        name = None

    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    emails = re.findall(email_pattern, text)
    email = emails[0] if emails else None

    phone_pattern = r"(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})"
    phones = re.findall(phone_pattern, text)
    phone = ''.join(phones[0]) if phones else None

    possible_skills = ['Python', 'SQL', 'Java', 'AWS', 'C++', 'JavaScript', 'HTML', 'CSS', 'Excel', 'Pandas', "AIML", 'AI/ML', 'CNN', 'AI', 'ML', 'Tensorflow', 'NumPy']
    skills = []
    for skill in possible_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            skills.append(skill)

    skills_string = ', '.join(skills)


    linkedin_url = None
    linkedin_pattern = r'(https?://)?(www\.)?linkedin\.com/[a-z]{2,4}/[A-Za-z0-9\-_/]+'
    for match in re.finditer(linkedin_pattern, text):
        url = match.group(0)
        if not url.startswith('http'):
            url = 'https://' + url
        linkedin_url = url
        break 

    git_hub = None
    git_hub_pattern = r'github\.com/([A-Za-z0-9\-_\/]+)'

    for match in re.finditer(git_hub_pattern, text):
        path = match.group(1)
        git_hub = f"https://github.com/{path}"
        break

    return name, email, phone, skills_string, linkedin_url, git_hub

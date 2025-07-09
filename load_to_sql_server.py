import pandas as pd
import pyodbc
import configparser as cp
import datetime

def connect(name, email, phone, skills, linkedin, github):

    config = cp.ConfigParser()
    config.read(r'C:\Users\mysur\OneDrive\Desktop\python_tutorial\venv1\config.config')

    DRIVER = config['ssms']['DRIVER']
    SERVER = config['ssms']['SERVER']
    DATABASE = config['ssms']['DATABASE']
    UID = config['ssms']['UID']
    PWD = config['ssms']['PWD']

    conn = pyodbc.connect(
            f'DRIVER={DRIVER};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            f'UID={UID};'
            f'PWD={PWD}'
    )

    cursor = conn.cursor()

    insert_query = """
    INSERT INTO resume_data (name, email, linkedin, github, phone, skills)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    cursor.execute(
    insert_query,
    name,
    email,
    linkedin,
    github,
    phone,
    skills
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    

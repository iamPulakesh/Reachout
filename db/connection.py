import os
import boto3
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_ssm_parameter(name, secure=False):
    ssm = boto3.client('ssm', region_name='ap-south-1')
    return ssm.get_parameter(Name=name, WithDecryption=secure)['Parameter']['Value']

# DB_HOST = get_ssm_parameter("/reachout/DB_HOST")
# DB_USER = get_ssm_parameter("/reachout/DB_USER")
# DB_PASSWORD = get_ssm_parameter("/reachout/DB_PASSWORD", secure=True)
# DB_NAME = get_ssm_parameter("/reachout/DB_NAME")

GOOGLE_MAPS_API_KEY = get_ssm_parameter("/reachout/GOOGLE_MAPS_API_KEY", secure=True)
S3_BASE_URL = get_ssm_parameter("/reachout/S3_BASE_URL")
BUCKET = get_ssm_parameter("/reachout/S3_BUCKET")

s3 = boto3.client('s3', region_name='ap-south-1')

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
    )

import boto3
import mysql.connector

def get_ssm_parameter(name, secure=False):
    ssm = boto3.client('ssm', region_name='ap-south-1')
    return ssm.get_parameter(Name=name, WithDecryption=secure)['Parameter']['Value']

DB_HOST = get_ssm_parameter("/reachout/DB_HOST")
DB_USER = get_ssm_parameter("/reachout/DB_USER")
DB_PASSWORD = get_ssm_parameter("/reachout/DB_PASSWORD", secure=True)
DB_NAME = get_ssm_parameter("/reachout/DB_NAME")
GOOGLE_MAPS_API_KEY = get_ssm_parameter("/reachout/GOOGLE_MAPS_API_KEY", secure=True)
S3_BASE_URL = get_ssm_parameter("/reachout/S3_BASE_URL")
BUCKET = get_ssm_parameter("/reachout/S3_BUCKET")

s3 = boto3.client('s3', region_name='ap-south-1')

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

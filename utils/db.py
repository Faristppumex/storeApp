import psycopg2
from psycopg2.extras import RealDictCursor
import boto3
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
# DYNAMO_DB_URL = os.getenv('DYNAMODB_URL')

def get_db():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def get_dynamo_db():
    return boto3.resource(
        'dynamodb',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
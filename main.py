import boto3  # pip install boto3
from dotenv import load_dotenv
import dynamo_s3
import os

load_dotenv()

ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('REGION_NAME')


def connect_AWS_Services() -> bool:
    try:
        # CONECTAR A LA BASE DE DATOS
        dynamo_s3.client_dynamodb = boto3.client('dynamodb',
                                                 aws_access_key_id=ACCESS_KEY_ID,
                                                 aws_secret_access_key=SECRET_ACCESS_KEY,
                                                 region_name=REGION_NAME)
        # CONECTAR A BUCKET S3 DE IMAGENES
        dynamo_s3.client_s3 = boto3.client('s3',
                                           aws_access_key_id=ACCESS_KEY_ID,
                                           aws_secret_access_key=SECRET_ACCESS_KEY,
                                           region_name=REGION_NAME)
    except:
        print('Something went wrong connecting with AWS')
        return False
    else:
        print('AWS Services running...')
        return True


def readFile(path: str) -> str:
    text_file = open(path, 'r')
    data = text_file.read()
    text_file.close()
    return data


if __name__ == '__main__':
    if connect_AWS_Services():
        # dynamo_s3.add_user('luisd', '0000', readFile('img1.txt'), 'Existiendo', ['Español', 'Inglés', 'Portugués'])
        # dynamo_s3.get_user('luisd')
        # dynamo_s3.deleteUser('luisd')
        pass

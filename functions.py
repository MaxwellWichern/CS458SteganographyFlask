import numpy as np
import boto3
from botocore.client import Config

def addNums(numOne, numTwo):
    return numOne + numTwo

def s3Connection():
    
    s3 = boto3.resource('s3',
                        aws_access_key_id = 'AKIASUMLVXC3TBX75UN7',
                        aws_secret_access_key = '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',
                        region_name='us-east-2'
                        )
    return s3

# def s3Upload(file, location):
#    s3 = s3Connection()
#   response = s3.meta.client.upload_file(file, 'stegosaurus', location)
#   return response

# def s3Delete(bucket, key):
#   s3 = s3Connection()
#   response = s3.meta.client.delete_object(Bucket = bucket, Key = key)
#   return response

def s3URL(bucket, key, region_name='us-east-2'):
    # Initialize the S3 client
    s3 = s3Connection()
    # Generate a pre-signed URL for the S3 object

    url = s3.meta.client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=3600  # URL will expire in 1 hour (you can adjust this as needed)
    )
    return url
    
def s3Upload(s3, bucket, path, key):

    s3.meta.client.upload_file(path, bucket, key)
    return (f"Uploaded {path} to s3://{bucket}/{key}")

def s3Delete(s3, bucket, key):

    s3.meta.client.delete_object(Bucket=bucket, Key=key)
    return(f"Removed s3://{bucket}/{key}")

def genUsersLinks(s3, bucket, user, imType):

    searchString = user + '/' + imType
    response = s3.meta.client.list_objects(Bucket=bucket, Prefix=searchString)
    return(response)
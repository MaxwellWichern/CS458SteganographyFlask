import numpy as np
import boto3

def addNums(numOne, numTwo):
    return numOne + numTwo

def s3Connection():
    s3 = boto3.resource('s3',
                        aws_access_key_id = 'AKIASUMLVXC3TBX75UN7',
                        aws_secret_access_key = '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'
                        )
    return s3

def s3Upload(file, location):
    s3 = s3Connection()
    response = s3.meta.client.upload_file(file, 'stegosaurus', location)
    return response

def s3Delete(bucket, key):
    s3 = s3Connection()
    response = s3.meta.client.delete_object(Bucket = bucket, Key = key)
    return response
import numpy as np
import boto3

def addNums(numOne, numTwo):
    return numOne + numTwo

def s3Connection():
    s3 = boto3.resource('s3',
                        aws_access_key_id = 'AKIASUMLVXC35BV5VD5D',
                        aws_secret_access_key = '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'
                        )
    return s3

def s3Upload(file, location):
    s3 = s3Connection()
    response = s3.meta.client.upload_file(file, 'stegosaurus', location)
    return response
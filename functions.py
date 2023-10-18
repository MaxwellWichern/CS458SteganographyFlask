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

# def s3Upload(file, location):
#    s3 = s3Connection()
#   response = s3.meta.client.upload_file(file, 'stegosaurus', location)
#   return response

# def s3Delete(bucket, key):
#   s3 = s3Connection()
#   response = s3.meta.client.delete_object(Bucket = bucket, Key = key)
#   return response

def s3URL(bucket, key):
    # Initialize the S3 client
    s3 = s3Connection()
    # Generate a pre-signed URL for the S3 object
    try:
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=3600  # URL will expire in 1 hour (you can adjust this as needed)
        )
        return url
    except Exception as e:
        print(f"Error generating URL for {key}: {e}")
        return None
    
def s3Upload(bucket, path, key):
    s3 = s3Connection()
    try:
        s3.upload_file(path, bucket, key)
        print(f"Uploaded {path} to s3://{bucket}/{key}")
    except Exception as e:
        print(f"Error uploading {path} to S3: {e}")

def s3Delete(bucket, key):
    s3 = s3Connection()
    try:
        s3.delete_object(Bucket=bucket, Key=key)
        print(f"Removed s3://{bucket}/{key}")
    except Exception as e:
        print(f"Error removing s3://{bucket}/{key}: {e}")
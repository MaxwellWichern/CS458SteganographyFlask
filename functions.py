import numpy as np
import boto3
from botocore.client import Config
import cv2
import datetime

def timeStamp():
# returns a string of the current time (year month day hr min sec microsec)
    stamp = datetime.datetime.now()
    return (stamp.strftime("%Y%m%d%H%M%S%f"))

def s3Connection():
# creates a connection to aws s3
    s3 = boto3.resource('s3',
                        aws_access_key_id = 'AKIASUMLVXC3TBX75UN7',
                        aws_secret_access_key = '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',
                        region_name='us-east-2',
                        config=Config(signature_version='s3v4')
                        )
    return s3

def s3URL(s3, bucket, key):
# Generate a pre-signed URL for the S3 object
    url = s3.meta.client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=3600  # URL will expire in 1 hour (you can adjust this as needed)
    )
    return url
    
def s3Upload(s3, bucket, path, key):
# Uploads file to s3 with image metadata
    fileType = path.split('.')
    if fileType[-1] == 'jpg':
        fileType[-1] = 'jpeg'

    with open(path, 'rb') as file:
        image_data = file.read()

    s3.meta.client.put_object(Bucket = bucket, Key = key, Body = image_data, ContentType=f'image/{fileType[-1]}')
    return (f"Uploaded {path} to s3://{bucket}/{key}")

def s3Delete(s3, bucket, key):
# Deletes key from s3 bucket
    s3.meta.client.delete_object(Bucket=bucket, Key=key)
    return(f"Removed s3://{bucket}/{key}")

def genUsersLinks(s3, bucket, user, imType):
# Returns a list of all object for user and imType
    searchString = user + '/' + imType
    response = s3.meta.client.list_objects(Bucket=bucket, Prefix=searchString)
    return(response)

# Steganography Functions Below


def encrypt(image_path, message_to_encrypt, tmpDir):

    input_image = cv2.imread(image_path)

    # Getting the dimensions of the image
    height, width, depth = input_image.shape

    # Changing our secret message into one long string of binary and removing the prefix
    # We loop through the message we are given and then convert each character
    # Once the character is in binary format we add it onto the binary_data string
    binary_data = "".join(format(ord(char), '08b') for char in message_to_encrypt)

    # Shaping our data into the length and width of the image that we will hide it in
    # This turns our data into a fake copy of the image with our data in the pixel matrix slots were we will hide them
    # We start our data string in the top left of the fake image and then work left to right top to bottom
    # Then we will fill the rest of the fake image with zeros
    binary_data = binary_data.ljust(height * width * 3, '0')

    # Converting our fake image string into a numpy array
    # Each char in the fake image string is its own element in the array
    binary_data = np.array(list(binary_data)).astype(int)

    # Here we reshape our fake image array into an array of matrices
    binary_data = binary_data.reshape((height, width, 3))

    # Modify the least significant bit of each channel in the image
    # Looping from top to bottom in the image
    for b in range(height):
        # Looping from left to right in the image
        for g in range(width):
            # The three channels are Blue, Green, and Red in that order
            # We loop through each of the three color channels and hide our hidden message within
            for r in range(3):
                input_image[b, g, r] = (input_image[b, g, r] & 0xFE) | binary_data[b, g, r]

    # Save the modified image
    fileName = timeStamp() + ".png"
    cv2.imwrite(tmpDir + '/' + fileName, input_image)

    # Printing to show that we have finished encoding
    return({'fileName': fileName})

def decrypt(image_path):

    hidden_image = cv2.imread(image_path)

    # Getting the dimensions of the image
    height, width, _ = hidden_image.shape

    # Initializing an empty numpy array
    # We also shape the array to be an array of matrices
    extracted_data = np.zeros((height, width, 3), int)

    # Pulling the binary data from the LSB of the image
    # Looping from top to bottom in the image
    for b in range(height):
        # Looping from left to right in the image
        for g in range(width):
            # The three channels are Blue, Green, and Red in that order
            # We loop through each of the three color channels and pull the LSB from each pixel
            for r in range(3):
                extracted_data[b, g, r] = hidden_image[b, g, r] & 1

    # This leaves us with tons of data and most of it is useless empty entries
    # The next task is to search through the data and delete empty entries

    # Reshaping the data we pulled from an array of 3x3 matrices into a 1D array
    extracted_data = extracted_data.flatten()
    
    # Convert the extracted binary data array into one long string
    extracted_data = "".join([str(bit) for bit in extracted_data])

    # Splitting it up into chunks of 8 characters to an entry
    chunks = [extracted_data[i:i+8] for i in range(0, len(extracted_data), 8)]

    # Converting the chunks of 8 characters into a numpy array so that we can use numpy functions on the data
    chunk_array = np.array(chunks)

    # We will use this next to search for empty entries and remove them
    empty_entry = "00000000"

    # Here we use the previous variable to search the array and then delete empty values
    if empty_entry in chunk_array:
        # Find the index of the element
        index_to_delete = np.where(chunk_array == empty_entry)[0]

        # Delete the element at the found index
        kinda_final_array = np.delete(chunk_array, index_to_delete)

    # Now that we have removed all the empty entries everything remaining will be translated back to words
    # Taking the numpy array of chunks and then returning them to one long string
    binary_string = ''.join(kinda_final_array)

    # Splitting the binary string into 8-bit chunks
    binary_chunks = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]

    # Convert each 8-bit binary chunk to its decimal representation and then to a character
    text = ''.join([chr(int(chunk, 2)) for chunk in binary_chunks])

    # Returning the message back to the main
    return {"message": text}
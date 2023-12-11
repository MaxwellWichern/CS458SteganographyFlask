import numpy as np
import cv2

def encrypt(input_image, message_to_encrypt):
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
    cv2.imwrite("RobustImage.png", input_image)

    # Printing to show that we have finished encoding
    print("finished hiding")

def decrypt(hidden_image):

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


# Load the initial image
image = cv2.imread("origInImg.png")

# Change the string in here to change what we are hiding in the image
hiddenMessage = "AHHHHH ;-; HHHHHA"

# Calling the funtion to encrypt our string into the image
# Passing it the image and the string that we will be using
encrypt(image, hiddenMessage)

# This is loading the image after it's encrypted
image2 = cv2.imread("RobustImage.png")

# Sending the streganographied? image to get decoded
hidden_message = decrypt(image2)

# Printing out the message that was hidden
print(hidden_message["message"])



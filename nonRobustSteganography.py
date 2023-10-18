import numpy as np
import cv2
#from scipy.fft import dctn, idctn
#import array as arr

#NOT CURRENTLY USING THIS FUNCTION AT ALL BUT PLEASE DON'T DELETE IT
def string_to_binary_array(input_string):
    #initializing an empty numpy array
    binary_array = np.zeros((0))

    for char in input_string:
        # Get the ASCII code for the character and convert it to binary
        # We use the [2:] part to get rid of the 0b prefix of the ASCII
        binary_representation = bin(ord(char))[2:]

        # Here we make sure that each binary entry is 8 characters long
        # We add leading zeros with the zfill if it is not the correct length
        binary_representation = binary_representation.zfill(8)

        # Add the binary entry to the array
        binary_array = np.append(binary_array, binary_representation)

    return binary_array


def encrypt(input_img, message_to_encrypt):
    # Getting the dimensions of the image
    height, width, _ = image.shape

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
    for i in range(height):
        # Looping from left to right in the image
        for j in range(width):
            # The three channels are Blue, Green, and Red in that order
            # We loop through each of the three color channels and hide our hidden message within
            for c in range(3):
                image[i, j, c] = (image[i, j, c] & 0xFE) | binary_data[i, j, c]

    # Save the modified image
    cv2.imwrite("nonRobustImage.png", image)

    # Printing to show that we have finished encoding
    print("finished hiding")

def decrypt(hidden_image):

    # Taking the image we are passed and reassigning it to a name I like better
    # Don't ask me why I only did this for this function
    image = hidden_image

    # Getting the dimensions of the image
    height, width, _ = image.shape

    # Initializing an empty numpy array
    # We also shape the array to be an array of matrices
    extracted_data = np.zeros((height, width, 3), int)

    # Pulling the binary data from the LSB of the image
    # Looping from top to bottom in the image
    for i in range(height):
        # Looping from left to right in the image
        for j in range(width):
            # The three channels are Blue, Green, and Red in that order
            # We loop through each of the three color channels and pull the LSB from each pixel
            for c in range(3):
                extracted_data[i, j, c] = image[i, j, c] & 1

    # This leaves us with tons of data and most of it is useless empty entries
    # The next task is to search through the data and delete empty entries

    # Reshaping the data we pulled from an array of 3x3 matrices into a 1D array
    extracted_data = extracted_data.flatten()

    # Convert the extracted binary data array into one long string
    extracted_data = "".join([str(bit) for bit in extracted_data])

    # Splitting it up into chunks of 8 characters to an entry
    chunks = [extracted_data[i:i+8] for i in range(0, len(extracted_data), 8)]

    # Converting the chunks of 8 characters into a numpy array so that we can use numpy functions on the data
    array_entry = np.array(chunks)

    # We will use this next to search for empty entries and remove them
    empty_entry = "00000000"

    # Here we use the previous variable to search the array and then delete empty values
    if empty_entry in array_entry:
        # Find the index of the element
        index_to_delete = np.where(array_entry == empty_entry)[0]

        # Delete the element at the found index
        my_array = np.delete(array_entry, index_to_delete)

    # Now that we have removed all the empty entries everything remaining will be translated back to words

    # Taking the numpy array of chunks and then returning them to one long string
    binary_string = ''.join(my_array)

    # Splitting the binary string into 8-bit chunks
    binary_chunks = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]

    # Convert each 8-bit binary chunk to its decimal representation and then to a character
    text = ''.join([chr(int(chunk, 2)) for chunk in binary_chunks])

    # Returning the message back to the main
    return {"message": text}


# Load the initial image
image = cv2.imread("rose.png")

# Change the string in here to change what we are hiding in the image
encrypt(image, "AHHHHH ;-; HHHHHA")
#encrypt(image, "80085")

# This is loading the image after it's encrypted
image2 = cv2.imread("nonRobustImage.png")

# Sending the streganographied? image to get decoded
hidden_message = decrypt(image2)

# Printing out the message that was hidden
print(hidden_message["message"])



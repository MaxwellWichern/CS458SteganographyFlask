import numpy as np
import cv2
from scipy.fft import dctn, idctn
import array as arr


def string_to_binary_array(input_string):
    binary_array = np.zeros((0))

    for char in input_string:
        # Get the ASCII code for the character and convert it to binary
        binary_representation = bin(ord(char))[2:]  # [2:] removes the '0b' prefix

        # Ensure that each binary representation is 8 characters long (pad with leading zeros if needed)
        binary_representation = binary_representation.zfill(8)

        # Add the binary representation to the array
        binary_array = np.append(binary_array, binary_representation)
        #print(binary_representation)
        #print(binary_array)

    return binary_array



def encrypt(input_img, message_to_encrypt):
    # Ensure the image and binary data have the same shape
    height, width, _ = image.shape
    binary_data = "".join(format(ord(char), '08b') for char in message_to_encrypt)

    binary_data = binary_data.ljust(height * width * 3, '0')  # Pad data if needed
    binary_data = np.array(list(binary_data)).astype(int)  # Convert to NumPy array
    binary_data = binary_data.reshape((height, width, 3))
    # Modify the least significant bit of each channel in the image
    for i in range(height):
        for j in range(width):
            for c in range(3):  # 3 color channels (BGR)
                image[i, j, c] = (image[i, j, c] & 0xFE) | binary_data[i, j, c]

    # Save the modified image
    cv2.imwrite("output_image.png", image)
    print("finished hiding")

def decrypt(hidden_image):
    # Load the image
    image = hidden_image
    height, width, _ = image.shape


    # Initialize an empty binary data array
    extracted_data = np.zeros((height, width, 3), int)

    # Extract the binary data from the LSB of the image
    for i in range(height):
        for j in range(width):
            for c in range(3):
                extracted_data[i, j, c] = image[i, j, c] & 1

    # Convert the extracted binary data to a string
    extracted_data = extracted_data.flatten()
    extracted_data = "".join([str(bit) for bit in extracted_data])
    #print("Extracted Binary Data:", extracted_data)
    chunks = [extracted_data[i:i+8] for i in range(0, len(extracted_data), 8)]
    empty_entry = "00000000"
    # Convert the chunks to a NumPy array
    array_entry = np.array(chunks)
    if empty_entry in array_entry:
        # Find the index of the element
        index_to_delete = np.where(array_entry == empty_entry)[0]
        # Delete the element at the found index
        my_array = np.delete(array_entry, index_to_delete)
        print(my_array)

    binary_string = ''.join(my_array)

    # Split the binary string into 8-bit chunks
    binary_chunks = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]

    # Convert each 8-bit binary chunk to its decimal representation and then to a character
    text = ''.join([chr(int(chunk, 2)) for chunk in binary_chunks])

    #print("Decoded Text:", text)
    return {"message": text}


# Load the initial image
image = cv2.imread("rose.png")
#this is loading the image after it's encrypted
image2 = cv2.imread("output_image.png")
#change the string in here to change what we are hiding in the image
encrypt(image, "testing")
hidden_message = decrypt(image2)
print(hidden_message["message"])
#print(first_eight_characters)
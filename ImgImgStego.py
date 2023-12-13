import numpy as np
import cv2

def encrypt(original_image, image_to_encrypt):
    # Getting the dimensions of the images
    height, width, depth = original_image.shape
    height2, width2, depth2 = image_to_encrypt.shape

    # Taking the dimensions of the image in binary and getting the size of the string
    # Then we also convert the size of that image to binary
    dimH = format(height2, '08b')
    dimW = format(width2, '08b')
    Dims = dimH + dimW
    DimsSize = len(Dims)
    DimsSizeBinary = format(DimsSize, '08b')

    index = 0
    tempindex = 0

    # Looping through each pixel of original_image
    for x in range(height2):
        for y in range(width2):
            for z in range(3):
                # This gives us the binary string representation of the current pixel
                # It also removes the 08b prefix from the binary string
                original_image_binary = format(original_image[x, y, z], '08b')

                # This gives us the binary string representation the pixel in the same position on the image to encrypt
                # It also removes the 08b prefix from the binary string
                image_to_encrypt_binary = format(image_to_encrypt[x, y, z], '08b')

                # Taking 5 MSBs from the first image and 3 MSBs from the second image
                # We then combine them to give us a single binary string
                final_image_binary = original_image_binary[:5] + image_to_encrypt_binary[:3]

                # Converting the binary string back to pixel values
                # Then we assign the new value to the current pixel
                original_image[x, y, z] = int(str(final_image_binary), 2)

    for x in range(height):
        for y in range(width):
            for z in range(3):
                original_image_binary = format(original_image[x, y, z], '08b')
                # Hiding the length of the binary dimensions in the bottom row
                # We also hide the actual dimensions in binary
                if (x == height - 1 and z == 0 and index < (DimsSize+9)):
                    if (index < 8):
                        final_image_binary = original_image_binary[:7] + DimsSizeBinary[index]
                        original_image[x, y, z] = int(str(final_image_binary), 2)
                    if (index > 8):
                        final_image_binary = original_image_binary[:7] + Dims[tempindex]
                        original_image[x, y, z] = int(str(final_image_binary), 2)
                        tempindex = tempindex + 1
                    index = index + 1

    # Writing the steganography image
    cv2.imwrite('outImgImg.png', original_image)

    # Printing to show that we have finished encoding
    print("finished hiding")

def decrypt(hidden_image):

    # Encrypted image
    height, width, depth = hidden_image.shape

    # Initializing variables
    tempstring = ""
    tempstringsize = ""

    # Creating an empty image with the same dimensions of the given image
    img2 = np.zeros((height, width, 3), np.uint8)

    # Looping through each pixel of the image
    for x in range(height):
        for y in range(width):
            for z in range(3):
                # Converting the current pixel to a binary string and getting rid of the '08b' prefix
                encoded_image_binary = format(hidden_image[x, y, z], '08b')

                # Pulling the 3 least significant bits that represent the 3 significant bits of the hidden image
                # We then add 00000 to the end of the image for better image reconstruction
                last_three_binary = encoded_image_binary[5:] + '00000'

                # Converting first_five_binary and last_three_binary to binary ints
                # We then place them into the empty images we created earlier
                img2[x, y, z] = int(str(last_three_binary), 2)

                tempholdsize = tempstringsize

                # Pulling out how many bits we have to grab in order to get the dimentions out
                if(x == height-1 and y < 8 and z == 0):
                    tempstringsize = tempholdsize + str(encoded_image_binary[7:])

    # This is going to be the number of bits we grab for the dimensions
    holddis = int(tempstringsize, 2)

    for x in range(height):
        for y in range(width):
            for z in range(3):
                # Converting the current pixel to a binary string and getting rid of the '08b' prefix
                encoded_image_binary = format(hidden_image[x, y, z], '08b')

                temphold = tempstring

                # tempstring is going to hold the binary of both the height and width dimensions
                if(x == height-1 and 8 < y and y < holddis+9 and z == 0):
                    tempstring = temphold + str(encoded_image_binary[7:])

    # Here we split the binary string into separate strings with each one representing a measurement
    hDim = tempstring[0:len(tempstring) // 2]
    wDim = tempstring[len(tempstring) // 2 if len(tempstring) % 2 == 0 else ((len(tempstring) // 2) + 1):]

    # Converting our dimensions from binary to usable numbers
    hDim = int(hDim, 2)
    wDim = int(wDim, 2)

    # Cropping the image using the dimensions we pulled earlier
    img2 = img2[:hDim, :wDim]

    # Returning the hidden image
    return img2

# Load the initial image
image = cv2.imread("pirate.jpg")

# Change the string in here to change what we are hiding in the image
Image_To_Hide = cv2.imread("cat.jpg")

# Calling the funtion to encrypt our string into the image
# Passing it the image and the string that we will be using
encrypt(image, Image_To_Hide)

# This is loading the image after it's encrypted
image2 = cv2.imread('outImgImg.png')

cv2.imshow("heres the hide", image2)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Sending the streganographied? image to get decoded
hidden_message = decrypt(image2)

cv2.imshow("heres the hidden", hidden_message)
cv2.waitKey(0)
cv2.destroyAllWindows()

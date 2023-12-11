import numpy as np
import random
import cv2

def encrypt(original_image, image_to_encrypt):
    # Getting the dimensions of the images
    height, width, depth = original_image.shape
    height2, width2, depth2 = image_to_encrypt.shape

    dimH = format(height2, '08b')
    dimW = format(width2, '08b')
    dimHLong = format(height2, '018b')
    #dimHLong = np.array(list(dimHLong)).astype(int)
    dimWLong = format(width2, '018b')
    #dimWLong = np.array(list(dimWLong)).astype(int)
    Dims = dimH + dimW
    #print(len(Dims))
    #print(Dims)

    index = 0

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

                #We're using the corner pixel for width
                if(x == height2-1 and y == 0):
                    print(dimWLong[5*z:5*(z+1)])
                    #print(format(original_image[x,y,0],'08b')[0:3] + dimWLong[5*z:5*(z+1)])
                    original_image[x,y,z] = format(original_image[x,y,0],'08b')[0:3] + dimWLong[5*z:5*(z+1)]

                if(x==height2-1 and y==1):
                    original_image[x, y, z] = format(original_image[x, y, 0], '08b')[0:3] + dimHLong[5*z:5*(z+1)]

#                if(x == height2-1 and y == 0):
#                    if len(Dims) >= 10:
#                        final_image_binary = original_image_binary[:6] + str(len(Dims))
#                        original_image[x, y, z] = int(str(final_image_binary), 2)
#                    if len(Dims) < 10:
#                        final_image_binary = original_image_binary[:7] + str(len(Dims))
#                        original_image[x, y, z] = int(str(final_image_binary), 2)

#                if(x == height2-1):
#                    if(index < len(Dims)):
#                        final_image_binary = original_image_binary[:7] + Dims[index]
#                        original_image[x, y, z] = int(str(final_image_binary), 2)
#                    index = index + 1
#                    if(index == len(Dims)):
#                        final_image_binary = original_image_binary[:7] + '0'
#                        original_image[x, y, z] = int(str(final_image_binary), 2)

    #print(format(original_image[height-1,0,0],'08b')[0:3]+dimWLong[0:5])
    #Hide width in the corner pixels
    original_image[height-2,0,0] = int(format(original_image[height-2,0,0],'08b')[0:5]+dimWLong[0:3])
    original_image[height-2,0,1] = int(format(original_image[height-2,0,1],'08b')[0:5]+dimWLong[3:6])
    original_image[height-2,0,2] = int(format(original_image[height-2,0,2],'08b')[0:5]+dimWLong[6:9])

    original_image[height - 1, 0, 0] = int(format(original_image[height - 1, 0, 0], '08b')[0:5] + dimWLong[9:12])
    original_image[height - 1, 0, 1] = int(format(original_image[height - 1, 0, 1], '08b')[0:5] + dimWLong[12:15])
    original_image[height - 1, 0, 2] = int(format(original_image[height - 1, 0, 2], '08b')[0:5] + dimWLong[15:18])

    #Hide heigth in the other corner pixels
    original_image[height-4,0,0] = int(format(original_image[height - 4, 0, 0], '08b')[0:5] + dimHLong[0:3])
    original_image[height-4,0,1] = int(format(original_image[height - 4, 0, 1], '08b')[0:5] + dimHLong[3:6])
    original_image[height-4,0,2] = int(format(original_image[height - 4, 0, 2], '08b')[0:5] + dimHLong[6:9])

    original_image[height - 3, 0, 0] = int(format(original_image[height - 3, 0, 0], '08b')[0:5] + dimHLong[9:12])
    original_image[height - 3, 0, 1] = int(format(original_image[height - 3, 0, 1], '08b')[0:5] + dimHLong[12:15])
    original_image[height - 3, 0, 2] = int(format(original_image[height - 3, 0, 2], '08b')[0:5] + dimHLong[15:18])

    print(dimWLong)
    print(dimHLong)

    # Writing the steganography image
    cv2.imwrite('outImgImg.png', original_image)

    # Printing to show that we have finished encoding
    #print("finished hiding")

def decrypt(hidden_image):

    # Encrypted image
    height, width, depth = hidden_image.shape

    blue = hidden_image[:,:,0]

    tempstring = ""
    dimWHidden = ""
    dimHHidden = ""

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

                temphold = tempstring

                #Getting the width dimension
                if(x == height-1 and y==0):
                    print(encoded_image_binary[5:8])
                    dimWHidden += encoded_image_binary[5:8]
                if(x == height-2 and y==0):
                    print(encoded_image_binary[5:8])
                    dimWHidden += encoded_image_binary[5:8]

                if(x == height-3 and y==0):
                    print(encoded_image_binary[5:8])
                    dimHHidden += encoded_image_binary[5:8]
                if(x == height-4 and y==0):
                    print(encoded_image_binary[5:8])
                    dimHHidden += encoded_image_binary[5:8]
#                if(x == height-1 and y < 17):
#                    tempstring = temphold + str(encoded_image_binary[7:])
                    #print(tempstring)

    print(dimWHidden)
    print(dimHHidden)

    width = int(dimWHidden,2)
    height = int(dimHHidden,2)
    img2 = img2[:height,:width]

    # Returning the hidden image
    return img2

# Load the initial image
image = cv2.imread("pirate.jpg")
#image = cv2.imread("clocktower.jpg")

# Change the string in here to change what we are hiding in the image
Image_To_Hide = cv2.imread("dog.jpg")

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

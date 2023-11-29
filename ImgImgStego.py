import numpy as np
import random
import cv2
import warnings

def encrypt(original_image, image_to_encrypt):
    # Getting the dimensions of the images
    height, width, depth = original_image.shape
    height2, width2, depth2 = image_to_encrypt.shape

    cv2.imshow("first", original_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imshow("second", image_to_encrypt)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    for x in range(height2):
        for y in range(width2):
            for z in range(3):
                # v1 and v2 are 8-bit pixel values
                # of img1 and img2 respectively
                v1 = format(original_image[x][y][z], '08b')

                v2 = format(image_to_encrypt[x][y][z], '08b')

                # Taking 5 MSBs from the first image and 3 MSBs from the second image
                v3 = v1[:5] + v2[:3]


                original_image[x][y][z] = int(v3, 2)

    cv2.imwrite('outImgImg.png', original_image)

    # Printing to show that we have finished encoding
    print("finished hiding")

def decrypt(hidden_image):

    # Encrypted image
    #tempimg = cv2.imread('testImg2.png')
    img = hidden_image
    height, width, depth = img.shape

    #filling our values with randoms 1s or 0s
    chr(random.randint(0, 1) + 48) * 5
    chr(random.randint(0, 1) + 48) * 3

    # img1 and img2 are two empty images
    img1 = np.zeros((height, width, 3), np.uint8)
    img2 = np.zeros((height, width, 3), np.uint8)

    for x in range(height):
        for y in range(width):
            for z in range(3):
                v1 = format(img[x][y][z], '08b')
                uhh = format(img[x][y-1][z], '08b')

                v2 = v1[:5] + chr(random.randint(0, 1) + 48) * 3
                v3 = v1[3:] + chr(random.randint(0, 1) + 48) * 5

                # Appending data to img1 and img2
                # Converting v2 and v3 to binary and then adding them to the end of the images
                img1[x][y][z] = int(v2, 2)
                img2[x][y][z] = int(v3, 2)

    cv2.imwrite('origInImg.png', img1)
    cv2.imwrite('origOutImg.png', img2)
    cv2.imshow("finalInImg", img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imshow("finalOutImg", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return img2

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load the initial image
image = cv2.imread("pirate.tif")
#image = cv2.imread("clocktower.jpg")

# Change the string in here to change what we are hiding in the image
Image_To_Hide = cv2.imread("testImg2.png")

# Calling the funtion to encrypt our string into the image
# Passing it the image and the string that we will be using
encrypt(image, Image_To_Hide)

# This is loading the image after it's encrypted
image2 = cv2.imread('outImgImg.png')

# Sending the streganographied? image to get decoded
hidden_message = decrypt(image2)

cv2.imshow("heres the hidden", hidden_message)
cv2.waitKey(0)
cv2.destroyAllWindows()

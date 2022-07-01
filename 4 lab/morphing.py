import numpy as np
import cv2
import math

'''
1- 2 images must have the same size .

2- we get the coordianates of the left and right eyes and mouse 
of 2 images

'''

# read image

img = cv2.imread(r"source\cat-1.png")
cv2.imshow("First", img)
cv2.waitKey(25)

img2 = cv2.imread(r"source\cat-3.png")
cv2.imshow("Second", img2)
cv2.waitKey(25)

# lift , right eyes and mouse
pts1 = np.array([[80, 139], [179, 141], [121, 198]], np.float32)
# [129, 132], [181, 129], [152, 151]
pts2 = np.array([[182, 121], [253, 125], [215, 168]], np.float32)

pts11 = np.zeros((3, 2), np.float32)
pts22 = np.zeros((3, 2), np.float32)

dis = 100.0  # iterations
piece = 0.5 / dis

for i in range(0, int(dis)):

    for j in range(0, 3):
        disx = (pts1[j, 0] - pts2[j, 0]) * -1
        disy = (pts1[j, 1] - pts2[j, 1]) * -1

        # move of first image
        movex1 = (disx / dis) * (i + 1)
        movey1 = (disy / dis) * (i + 1)

        # move of second image
        movex2 = disx - movex1
        movey2 = disy - movey1

        pts11[j, 0] = pts1[j, 0] + movex1
        pts11[j, 1] = pts1[j, 1] + movey1

        pts22[j, 0] = pts2[j, 0] - movex2
        pts22[j, 1] = pts2[j, 1] - movey2

    mat1 = cv2.getAffineTransform(pts1, pts11)
    mat2 = cv2.getAffineTransform(pts2, pts22)

    dst1 = cv2.warpAffine(img, mat1, (img.shape[1], img.shape[0]), None, None, cv2.BORDER_REPLICATE)
    dst2 = cv2.warpAffine(img2, mat2, (img.shape[1], img.shape[0]), None, None, cv2.BORDER_REPLICATE)

    dst = cv2.addWeighted(dst1, 1 - (piece * (i)), dst2, piece * (i + 1), 0)

    cv2.imshow("Morphing", dst)
    cv2.waitKey(25)

cv2.waitKey(0)
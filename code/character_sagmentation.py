import cv2
import numpy as np
import os
import glob
import pytesseract
from PIL import Image


def character_segmentation(img_path):
    for file in glob.glob(os.path.join('./characters/', '*')):
        os.remove(file)
    img = cv2.imread(img_path)
    cv2.imshow('in', img)
    height, width = img.shape[:2]
    im2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #ret,thresh = cv2.threshold(median_blur,127,255,cv2.THRESH_BINARY)
    ret2, thresh = cv2.threshold(im2, 127, 255, cv2.THRESH_OTSU)
    cv2.imshow('threshoulding',thresh)

    mask = np.zeros((height + 2, width + 2), np.uint8)
    # Floodfill from point (0, 0)
    im_floodfill = thresh.copy()
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)
    cv2.imshow("floodfill",im_floodfill)
    kernel = np.ones((13,2),np.uint8)
    erosion = cv2.erode(im_floodfill,kernel,iterations = 1)
    cv2.imshow("erosion",erosion)

    im_floodfill_inv = cv2.bitwise_not(erosion)
    cv2.imshow("floodfill_inv",im_floodfill_inv)

    # find contours
    im2, ctrs, hier = cv2.findContours(im_floodfill_inv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Getting ROI
        roi = img[y:y + h, x:x + w]

        # show ROI
        # cv2.imshow('segment no:'+str(i),roi)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,0), 1)
        # cv2.waitKey(0)

        if w < 7 or h < 7 or w*h>1500:
            if i!=1:
                i=i-1
            continue

        cv2.imwrite('./characters/{}.jpg'.format(i), roi)
    cv2.imshow('marked areas',img)
    #cv2.imwrite('img_contouring.png',img)
    return
"""
#text extraction logic begins from here..........
Img = Image.open('dhruv_car.jpeg')
text = pytesseract.image_to_string(Img)
print(text)"""

character_segmentation('frame350_2.jpg')
cv2.waitKey(0)

import numpy as np
import cv2
from skimage import measure
from skimage.measure import regionprops

def preprocess(img):
    #cv2.imshow("Input", img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    median_blur = cv2.medianBlur(gray,1)
    #cv2.imshow('median_blur', median_blur)

    equal_histogram = cv2.equalizeHist(median_blur)
    #cv2.imshow("After Histogram equalisation", equal_histogram)

    ret2, threshold_img = cv2.threshold(equal_histogram, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #cv2.imshow("Threshold", threshold_img)

    kernel = np.ones((2,2), np.uint8)
    closing = cv2.morphologyEx(threshold_img, cv2.MORPH_CLOSE, kernel)

    #erosion = cv2.erode(threshold_img, kernel, iterations=1)
    #cv2.imshow("closing", closing)
    # cv2.waitKey(0)
    return threshold_img

def isMaxWhite(plate):
    avg = np.mean(plate)
    if (avg >= 115):
        return True
    else:
        return False

def image_countouring(i,img,th_img):
    label_image = measure.label(th_img)
    plate_dimensions = (0.05 * label_image.shape[0], 0.15 * label_image.shape[0], 0.10 * label_image.shape[1], 0.30 * label_image.shape[1])
    min_height, max_height, min_width, max_width = plate_dimensions
    plate_objects_cordinates = []
    plate_like_objects = []

    for region in regionprops(label_image):
        if region.area < 50:
            # if the region is so small then it's likely not a license plate
            continue

        # the bounding box coordinates
        min_row, min_col, max_row, max_col = region.bbox
        region_height = max_row - min_row
        region_width = max_col - min_col

        # ensuring that the region identified satisfies the condition of a typical license plate
        if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
            plate_like_objects.append(th_img[min_row:max_row, min_col:max_col])
            plate_objects_cordinates.append((min_row, min_col, max_row+2, max_col+2))
            cv2.rectangle(img, (min_col, min_row), (max_col, max_row), (0,0,0),1)
            #cv2.imshow("Image contouring", img)

    l=len(plate_objects_cordinates)
    no_white_pixels=[]
    if l==1:
        crop_img = img[plate_objects_cordinates[0][0]:plate_objects_cordinates[0][2],plate_objects_cordinates[0][1]:plate_objects_cordinates[0][3]]
        im_re = cv2.resize(crop_img, (200,80))
        Target = "./number_plate/"+str(i)+".jpg"
        cv2.imwrite(Target, im_re)
    elif l != 0 and l != 1:
        count = 1
        for c in range(0,l):
            crop_img = img[plate_objects_cordinates[c][0]:plate_objects_cordinates[c][2],plate_objects_cordinates[c][1]:plate_objects_cordinates[c][3]]
            im_re = cv2.resize(crop_img, (200,80))
            Target = "./number_plate/"+str(i)+"_"+str(count)+".jpg"
            cv2.imwrite(Target, im_re)
            count=count+1

    cv2.waitKey(0)

"""if __name__ == '__main__':
    img_path="mycar2.jpeg"
    img = cv2.imread(img_path)
    img = cv2.resize(img, (500,400))
    threshold_img = preprocess(img)
    image_countouring(img,threshold_img)

"""






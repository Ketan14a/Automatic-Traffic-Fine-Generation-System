import cv2
import string
import os
import tensorflow as tf
import keras
import numpy as np
import glob

def prepare(filepath):
	IMG_SIZE = 28
	img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
	new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
	return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

def extractNumber():
	CLASSES = []
	for i in range(0,10):
		CLASSES.append(str(i))

	ALPHA = string.ascii_uppercase

	for i in ALPHA:
		CLASSES.append(i)

	model = tf.keras.models.load_model('Mymodel.model')
	Ans = ""
	img_List = glob.glob(os.path.join('./characters/', '*.jpg'))
	for im in sorted(img_List):
		prediction = model.predict([prepare(im)])
		val = np.array(prediction[0])
		maxpos = np.argmax(val)
		Ans = Ans + CLASSES[maxpos]
	return Ans

"""A = extractNumber()

print("The number on the number-plate is "+A)"""


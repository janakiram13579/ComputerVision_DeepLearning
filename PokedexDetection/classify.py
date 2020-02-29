#Uasage-- Classify the images using trained model
#import all necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils, cv2, os, pickle

#construct argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model",required=True,help="path to trained model")
ap.add_argument("-l", "--labelbin",required=True,help="path to the label binarizer")
ap.add_argument("-i","--image",required=True,help="path to the image")
args=vars(ap.parse_args())

#load the images
image = cv2.imread(args["image"])
output = image.copy()

#pre=process the image for classification
image = cv2.resize(image,(96,96))
image = image.astype("float") / 255.0
image = img_to_array(image)
image = np.expand_dims(image, axis =0)

#load the trained model and label binarizer
model = load_model(args["model"])
lb = pickle.loads(open(args["labelbin"], "rb").read())

#classify the input image
print("[INFO] classifying the image..")
proba = model.predict(image)[0]
idx = np.argmax(proba)
label = lb.classes_[idx]
print(label)

#rest of the code is for display the text on top of the image
filename = args["image"][args["image"].rfind(os.path.sep)+ 1:]
correct = "correct" if filename.rfind(label) != -1 else "incorrect"

#build the label and draw on the image
label = "{}: {:.2f}% ({})".format(label, proba[idx] * 100, correct)
output = imutils.resize(output, width=400)
cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,0.7, (0, 255, 0), 2)

#show the output
print("[INFO] {}".format(label))
cv2.imshow("Output", output)
cv2.waitKey(0)
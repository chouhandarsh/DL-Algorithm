import tensorflow
from tensorflow import keras
from keras.models import load_model
model = load_model("/mnt/d/DL-Algorithm/functional-API/age_gender_model.keras")
import cv2 as cv
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Error: Camera not found")
else:
    while True:
        ret,frame = cap.read()
        if not ret:
            print("Error: could not load image")
            break
        cv.imshow("Camera",ret)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()



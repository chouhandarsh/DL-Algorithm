import keras
from keras.applications.resnet50 import ResNet50
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

model = ResNet50(weights='imagenet')

img_path = r"/mnt/d/DL-Algorithm/CNN/image copy 2.png"
img = keras.utils.load_img(img_path, target_size=(224, 224))
x = keras.utils.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)
import cv2 as cv
import numpy as np

camera = cv.VideoCapture(0)
if not camera.isOpened():
    raise RuntimeError("Could not open the camera. Check camera permissions and try camera index 1.")

print("Camera ready. Press SPACE to capture an image or Q to cancel.")
captured_frame = None

try:
    while True:
        success, frame = camera.read()
        if not success:
            raise RuntimeError("Could not read a frame from the camera.")

        cv.imshow("Camera - SPACE to capture, Q to cancel", frame)
        key = cv.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        if key == 32:
            captured_frame = frame.copy()
            break
finally:
    camera.release()
    cv.destroyAllWindows()

if captured_frame is not None:
    cv.imwrite("camera_capture.jpg", captured_frame)

    # OpenCV captures BGR images; ResNet50 expects RGB images.
    rgb_frame = cv.cvtColor(captured_frame, cv.COLOR_BGR2RGB)
    rgb_frame = cv.resize(rgb_frame, (224, 224))
    x = np.expand_dims(rgb_frame.astype("float32"), axis=0)
    x = preprocess_input(x)

    predictions = model.predict(x, verbose=0)
    print("Predicted:")
    for _, label, probability in decode_predictions(predictions, top=3)[0]:
        print(f"{label}: {probability:.2%}")
else:
    print("No image was captured.")
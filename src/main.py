import cv2
import numpy as np
import time

from darknet_detector import DarknetDetector
from flask import Flask, render_template, request, make_response

app = Flask(__name__)
app.jinja_env.auto_reload = True

# yolo_detector = DarknetDetector(
#     config_path="./models/yolov4.cfg",
#     weight_path="./models/yolov4.weights",
#     meta_path="./models/coco.data",
# )

# plate_detector = DarknetDetector(
#     config_path="./models/yolov4-plate-test.cfg",
#     weight_path="./models/yolov4-plate.weights",
#     meta_path="./models/plate.data",
# )

# characters_detector = DarknetDetector(
#     config_path="./models/yolov4-characters-test.cfg",
#     weight_path="./models/yolov4-characters.weights",
#     meta_path="./models/characters.data",
# )
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/yolo')
def yolo():
    return render_template('detector.html', title="YOLOv4")

@app.route('/yolo/upload', methods = ["POST"])
def process_yolo():
    global yolo_detector
    f = request.files['image'].read()
    im = cv2.imdecode(np.frombuffer(f, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    # detections = yolo_detector.detect(im)
    # for detection in detections:
    #     x1, y1, x2, y2 = detection.bbox
    #     cv2.rectangle(im, (x1, y1), (x2, y2), (255, 0, 0), 1)
    #     cv2.putText(
    #         im, detection.name, (x1, y2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 145), 1
    #     )

    _, buf = cv2.imencode(".jpg", im)
    response = make_response(buf.tobytes())
    response.headers["Content-Type"] = "image/jpeg"
    return response

@app.route('/plate')
def plate():
    return render_template('detector.html', title="Plate")

@app.route('/plate/upload', methods = ["POST"])
def process_plate():
    global plate_detector
    global characters_detector

    f = request.files['image'].read()
    im = cv2.imdecode(np.frombuffer(f, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    # detections = plate_detector.detect(im)
    # for detection in detections:
    #     print(detection.name)
    #     x1, y1, x2, y2 = detection.bbox
    #     cv2.rectangle(im, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #     plate_img = im[y1:y2, x1:x2]
    #     chars = characters_detector.detect(plate_img)
    #     for char in chars:
    #         print(char.name)
    #         x1, y1, x2, y2 = char.bbox
    #         cv2.rectangle(plate_img, (x1, y1), (x2, y2), (255, 0, 0), 1)
    #         cv2.putText(
    #             plate_img, char.name, (x1, y2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 145), 1
    #         )

    cv2.putText(im, "FAKFOAKFOA", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)

    time.sleep(2)

    _, buf = cv2.imencode(".jpg", im)
    response = make_response(buf.tobytes())
    response.headers["Content-Type"] = "image/jpeg"
    return response

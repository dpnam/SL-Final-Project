import cv2
import numpy as np
import time

from darknet_detector import DarknetDetector
from flask import Flask, render_template, request, make_response

app = Flask(__name__)

yolo_detector = DarknetDetector(
    config_path="./models/yolov4.cfg",
    weight_path="./models/yolov4.weights",
    meta_path="./models/coco.data",
)

plate_detector = DarknetDetector(
    config_path="./models/yolov4-plate.cfg",
    weight_path="./models/yolov4-plate.weights",
    meta_path="./models/plate.data",
)

characters_detector = DarknetDetector(
    config_path="./models/yolov4-characters.cfg",
    weight_path="./models/yolov4-characters.weights",
    meta_path="./models/characters.data",
)
 
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
    detections = yolo_detector.detect(im)
    for detection in detections:
        x1, y1, x2, y2 = detection.bbox
        cv2.rectangle(im, (x1, y1), (x2, y2), (255, 0, 0), 1)
        cv2.putText(
            im, detection.name, (x1, y2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
        )

    _, buf = cv2.imencode(".jpg", im)
    response = make_response(buf.tobytes())
    response.headers["Content-Type"] = "image/jpeg"
    return response

@app.route('/plate')
def plate():
    return render_template('detector.html', title="Plate")

def drawToRect(im, str, bbox):
    # https://stackoverflow.com/a/50356242
    x1, y1, x2, y2 = bbox
    box_width = x2 - x1
    box_height = y2 - y1
    (text_width, text_height), baseline = cv2.getTextSize(str, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 1);
    scalex = box_width / text_width
    scaley = box_height / text_height
    scale = min(scalex, scaley);
    marginx = 0 if scale == scalex else int(box_width * (scalex - scale) / scalex * 0.5)
    marginy = 0 if scale == scaley else int(box_height * (scaley - scale) / scaley * 0.5)
    cv2.putText(im, str, (x1 + marginx, y2 - marginy), cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 255, 0), 1, 8, False);

def draw_chars(im, chars, plate_bbox):
    y_min = min(char.bbox[1] for char in chars)
    y_max = max(char.bbox[1] for char in chars)
    middle = (y_min + y_max) / 2
    for char in chars:
        x1, y1, x2, y2 = char.bbox
        top = y1 <= middle

        x1 += plate_bbox[0]
        y1 += plate_bbox[1]
        x2 += plate_bbox[0]
        y2 += plate_bbox[1]
        h = y2 - y1

        cv2.rectangle(im, (x1, y1), (x2, y2), (255, 0, 0), 1)

        if top:
            drawToRect(im, char.name, (x1, plate_bbox[1] - h, x2, plate_bbox[1]))
        else:
            drawToRect(im, char.name, (x1, plate_bbox[3], x2, plate_bbox[3] + h))

@app.route('/plate/upload', methods = ["POST"])
def process_plate():
    global plate_detector
    global characters_detector

    f = request.files['image'].read()
    im = cv2.imdecode(np.frombuffer(f, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    detections = plate_detector.detect(im)
    for detection in detections:
        x1, y1, x2, y2 = detection.bbox
        cv2.rectangle(im, (x1, y1), (x2, y2), (0, 255, 0), 1)
        plate_im = im[y1:y2, x1:x2]
        chars = characters_detector.detect(plate_im)
        draw_chars(im, chars, detection.bbox)

    _, buf = cv2.imencode(".jpg", im)
    response = make_response(buf.tobytes())
    response.headers["Content-Type"] = "image/jpeg"
    return response

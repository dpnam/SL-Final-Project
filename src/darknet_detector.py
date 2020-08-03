import darknet
import cv2


class Detection:
    def __init__(self, name, confidence, bbox):
        self.name = name
        self.confidence = confidence
        self.bbox = bbox


class DarknetDetector:
    def __init__(self, config_path, weight_path, meta_path):
        self.net_main = darknet.load_net_custom(
            config_path.encode("ascii"), weight_path.encode("ascii"), 0, 1
        )
        self.meta_main = darknet.load_meta(meta_path.encode("ascii"))
        self.network_width = darknet.network_width(self.net_main)
        self.network_height = darknet.network_height(self.net_main)

    @staticmethod
    def yolo_to_xyxy(x, y, w, h):
        x1 = int(round(x - (w / 2)))
        y1 = int(round(y - (h / 2)))

        x2 = int(round(x + (w / 2)))
        y2 = int(round(y + (h / 2)))

        return x1, y1, x2, y2

    @staticmethod
    def yolo_detections_to_detections(yolo_dets):
        detections = []
        for det in yolo_dets:
            name = det[0].decode('ascii')
            conf = det[1]
            x_center, y_center, w, h = det[2][0], det[2][1], det[2][2], det[2][3]
            bbox = DarknetDetector.yolo_to_xyxy(float(x_center), float(y_center), float(w), float(h))

            detections.append(Detection(name, conf, bbox))

        return detections

    def detect(self, im):
        im_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        im_resized = cv2.resize(
            im_rgb,
            (self.network_width, self.network_height),
            interpolation=cv2.INTER_LINEAR,
        )

        darknet_image = darknet.make_image(
            self.network_width, self.network_height, 3
        )
        darknet.copy_image_from_bytes(darknet_image, im_resized.tobytes())

        yolo_detections = darknet.detect_image(
            self.net_main, self.meta_main, darknet_image, thresh=0.75
        )

        detections = DarknetDetector.yolo_detections_to_detections(yolo_detections)

        h, w = im.shape[:2]
        width_ratio = w / self.network_width
        height_ratio = h / self.network_height

        scale = (width_ratio, height_ratio, width_ratio, height_ratio)

        for detection in detections:
            detection.bbox = tuple(int(l * r) for l, r in zip(detection.bbox, scale))

        return detections



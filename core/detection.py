import math
from ultralytics import YOLO

class LicensePlateDetector:
    def __init__(self, model_path, class_names, conf_threshold):
        self.model = YOLO(model_path)
        self.class_names = class_names
        self.conf_threshold = conf_threshold

    def detect(self, frame):
        detections = []
        results = self.model.predict(frame, conf=self.conf_threshold)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = math.ceil(box.conf[0] * 100) / 100
                cls_id = int(box.cls[0])
                cls_name = self.class_names[cls_id]

                detections.append({
                    "bbox": (x1, y1, x2, y2),
                    "confidence": conf,
                    "class": cls_name
                })

        return detections

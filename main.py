import cv2
import argparse
from datetime import datetime

from config import *
from core.detection import LicensePlateDetector
from core.ocr import LicensePlateOCR
from core.storage.json import JSONStorage
from core.storage.DB import DatabaseStorage

# ---------- CLI ARGUMENT ----------
parser = argparse.ArgumentParser(description="ANPR System")
parser.add_argument(
    "--source",
    type=str,
    required=True,
    help="Path to video file or camera index (0,1...)"
)
args = parser.parse_args()

# ---------- VIDEO SOURCE ----------
source = args.source
if source.isdigit():
    source = int(source)

cap = cv2.VideoCapture(source)

# ---------- MODULE INIT ----------
detector = LicensePlateDetector(MODEL_PATH, CLASS_NAMES, CONF_THRESHOLD)
ocr_engine = LicensePlateOCR()
json_storage = JSONStorage(JSON_DIR)
db_storage = DatabaseStorage(DB_PATH)

start_time = datetime.now()
license_plates = set()

# ---------- MAIN LOOP ----------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = detector.detect(frame)

    for det in detections:
        bbox = det["bbox"]
        plate_text = ocr_engine.recognize(frame, bbox)

        if plate_text:
            license_plates.add(plate_text)

        x1, y1, x2, y2 = bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, plate_text, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255), 2)

    if (datetime.now() - start_time).seconds >= SAVE_INTERVAL_SECONDS:
        json_storage.save(license_plates, start_time, datetime.now())
        db_storage.save(license_plates, start_time, datetime.now())
        license_plates.clear()
        start_time = datetime.now()

    cv2.imshow("ANPR System", frame)
    if cv2.waitKey(1) & 0xFF == ord("1"):
        break

cap.release()
cv2.destroyAllWindows()

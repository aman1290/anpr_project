import easyocr
import cv2
import re

class LicensePlateOCR:
    def __init__(self):
        # English only (fast & accurate for plates)
        self.reader = easyocr.Reader(['en'], gpu=False)

    def recognize(self, frame, bbox):
        x1, y1, x2, y2 = bbox
        crop = frame[y1:y2, x1:x2]

        # ---------- Preprocess ----------
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # ---------- OCR ----------
        results = self.reader.readtext(gray, detail=1)

        best_text = ""
        best_conf = 0

        for (bbox, text, conf) in results:
            if conf > best_conf:
                best_conf = conf
                best_text = text

        return self._clean_text(best_text)

    def _clean_text(self, text):
        text = text.upper()
        text = re.sub('[^A-Z0-9]', '', text)
        text = text.replace("O", "0")
        return text

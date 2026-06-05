import io
import cv2
import numpy as np
from ultralytics import YOLO


class LicensePlateDetector:
    def __init__(
        self, model_path: str, conf_threshold: float = 0.25, img_size: int = 800
    ):

        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.img_size = img_size

        dummy_img = np.zeros((640, 640, 3), dtype=np.uint8)
        self.model.predict(dummy_img, verbose=False)

    def predict(self, image_bytes: bytes) -> dict:

        try:
            np_arr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            results = self.model.predict(
                source=img, conf=self.conf_threshold, imgsz=self.img_size, verbose=False
            )
            boxes_data = results[0].boxes

            detected_plates = []

            for box in boxes_data:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                conf = float(box.conf[0].cpu().numpy())

                detected_plates.append(
                    {
                        "coordinates": [int(x1), int(y1), int(x2), int(y2)],
                        "confidence": round(conf, 3),
                    }
                )

            return {
                "status": "success",
                "total_plates_found": len(detected_plates),
                "plates": detected_plates,
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

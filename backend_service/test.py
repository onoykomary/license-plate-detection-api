from backend_service.core.model_runner import LicensePlateDetector
from backend_service.core.config import settings

def main():

    detector = LicensePlateDetector(
        model_path=settings.MODEL_PATH,
        conf_threshold=0.3,
    )

    image_path = "000054_0.jpg"

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    result = detector.predict(image_bytes)
    print(result)


if __name__ == "__main__":
    main()

from .celery_app import celery_app
from backend_service.core.s3_client import sync_s3_client
from backend_service.core.model_runner import LicensePlateDetector
from backend_service.core.config import settings

from backend_service.db.models import PlateMetadata
from backend_service.db.engine import SessionLocal

detector = LicensePlateDetector(
    model_path=settings.MODEL_PATH,
    conf_threshold=settings.CONF_THRESHOLD,
    img_size=settings.IMG_SIZE,
)


@celery_app.task(name="detect_license_plate")
def detect_task(file_id: str, task_id: str):

    db = SessionLocal() 
        
    try:
        image_bytes = sync_s3_client.download_file(file_id)
        result = detector.predict(image_bytes)

        record = PlateMetadata(
            task_id=task_id,
            file_id=file_id,
            status=result["status"],
            results=result.get("plates", []),
        )
        db.add(record)
        db.commit()

        return result
    
    except Exception as e:
        db.rollback() 
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()

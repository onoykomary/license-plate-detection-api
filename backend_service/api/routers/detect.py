from backend_service.api.schemas import (
    AsyncTaskResponse,
    TaskResultResponse,
)
from backend_service.core.s3_client import async_s3_client
from backend_service.worker.tasks import detect_task
import uuid
from backend_service.worker.celery_app import celery_app
from backend_service.db.engine import SessionLocal
from backend_service.db.models import PlateMetadata
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    with SessionLocal() as db:
        yield db

@router.post("/predict", response_model=AsyncTaskResponse)
async def predict(uploaded_file: UploadFile):
    # file ID
    file_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    # load file to S3
    content = await uploaded_file.read()
    await async_s3_client.upload_file(content, file_id)
    # celery run
    detect_task.apply_async(args=[file_id, task_id], task_id=task_id)
    return {"task_id": task_id, "status": "pending"}


@router.get("/result/{task_id}", response_model=TaskResultResponse)
def get_status(task_id: str, db: Session = Depends(get_db)):

    record = db.query(PlateMetadata).filter(PlateMetadata.task_id == task_id).first()
    if record:
        result_data = {
            "status": record.status, 
            "plates": record.results,
            "total_plates_found": len(record.results) if record.results else 0
        }
        return {"task_id": task_id, "status": "SUCCESS", "result": result_data}
    
    task_result = celery_app.AsyncResult(task_id)

    return {"task_id": task_id, "status": task_result.state}


# uvicorn main:app --reload

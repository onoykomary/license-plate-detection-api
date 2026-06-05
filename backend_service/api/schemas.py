from pydantic import BaseModel
from typing import List, Optional


class PlatePrediction(BaseModel):
    coordinates: List[int]
    confidence: float


class PredictResponse(BaseModel):
    status: str
    total_plates_found: int = None
    plates: List[PlatePrediction] = None
    message: Optional[str] = None


class AsyncTaskResponse(BaseModel):
    task_id: str
    status: str


class TaskResultResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[PredictResponse] = None

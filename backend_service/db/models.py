from sqlalchemy import Column, String, JSON
from .engine import Base


class PlateMetadata(Base):
    __tablename__ = "plate_metadata"
    task_id = Column(String, primary_key=True, index=True)
    file_id = Column(String, index=True)
    status = Column(String)
    results = Column(JSON)

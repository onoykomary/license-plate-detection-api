from fastapi import FastAPI
from backend_service.api.routers.detect import router as plate_router
from backend_service.db.engine import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(plate_router, prefix="/model")

@app.get("/")
def health():
    return {"status": "alive"}

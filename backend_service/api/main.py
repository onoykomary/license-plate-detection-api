from fastapi import FastAPI
from backend_service.api.routers.detect import router as plate_router
from backend_service.db.engine import engine, Base
from contextlib import asynccontextmanager
from backend_service.core.s3_client import async_s3_client

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await async_s3_client.create_bucket_if_not_exists()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(plate_router, prefix="/model")

@app.get("/")
def health():
    return {"status": "alive"}

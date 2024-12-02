from fastapi import FastAPI
from routers import files
from database import engine, Base
from logger import logger

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Media Service")


@app.on_event("startup")
async def startup_event():
    logger.info("Start")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Stop")


app.include_router(files.router)

from fastapi import FastAPI
from routers import files
from database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Media Service")

app.include_router(files.router)

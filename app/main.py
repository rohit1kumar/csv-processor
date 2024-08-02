from fastapi import FastAPI
from dotenv import load_dotenv
from . import models
from .database import engine
from .router import router
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Go to /docs to see the API documentation"}


@app.get("/health")
def health_check():
    return {"message": "Chicken dinner!"}

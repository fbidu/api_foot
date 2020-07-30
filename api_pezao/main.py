"""
Here be awesome code!
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import auth, files, hospitals, logs, results, sms, users

Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

app.include_router(auth.router)
app.include_router(files.router)
app.include_router(hospitals.router)
app.include_router(logs.router)
app.include_router(results.router)
app.include_router(sms.router)
app.include_router(users.router)


origins = ["http://localhost:3000", "http://localhost", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    """
    The root of the API
    """
    return "Hello, world!"

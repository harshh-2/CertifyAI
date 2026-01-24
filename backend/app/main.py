from fastapi import FastAPI

app = FastAPI(title="CertifyAI Backend")

@app.get("/")
def root():
    return {"message": "CertifyAI backend is running"}
from fastapi import FastAPI

from routes import auth

app = FastAPI(title="CertifyAI Backend")

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "CertifyAI backend is running"}

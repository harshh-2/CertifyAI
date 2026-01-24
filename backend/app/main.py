from fastapi import FastAPI
from backend.config.db import client

app = FastAPI(title="CertifyAI Backend")

@app.on_event("startup")
async def startup_db():
    await client.admin.command("ping")
    print("MongoDB connected")

@app.on_event("shutdown")
async def shutdown_db():
    client.close()

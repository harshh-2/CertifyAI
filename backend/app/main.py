from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.config.db import client
from backend.routes import auth, recommend  # This pulls from backend/app/routes/

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs when the server starts
    try:
        await client.admin.command("ping")
        print("✅ Backend connected to MongoDB Atlas")
    except Exception as e:
        print(f"❌ DB Connection Error: {e}")
    yield
    # This runs when the server stops
    client.close()

app = FastAPI(title="CertifyAI API", lifespan=lifespan)

# Connect your routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(recommend.router, prefix="/certs", tags=["Certifications"])
@app.get("/")
async def health_check():
    return {"status": "online", "database": "connected"}
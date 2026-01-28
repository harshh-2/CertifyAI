from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from config.db import client
from routes import auth, recommend, vault


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        await client.admin.command("ping")
        print("✅ Backend connected to MongoDB Atlas")
    except Exception as e:
        print(f"❌ DB Connection Error: {e}")

    yield

    client.close()
    print("🛑 MongoDB connection closed")


app = FastAPI(
    title="CertifyAI API",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-session-key"
)


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(recommend.router, prefix="/certs", tags=["Certifications"])
app.include_router(vault.router, tags=["Vault"])


@app.get("/")
async def health_check():
    return {
        "status": "online",
        "database": "connected"
    }

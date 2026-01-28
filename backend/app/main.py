from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from config.db import client
from routes import auth, recommend, vault


# ---------------- Lifespan (Startup / Shutdown) ----------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    # On server start
    try:
        await client.admin.command("ping")
        print("✅ Backend connected to MongoDB Atlas")
    except Exception as e:
        print(f"❌ DB Connection Error: {e}")

    yield

    # On server shutdown
    client.close()
    print("🛑 MongoDB connection closed")


# ---------------- App Init ----------------

app = FastAPI(
    title="CertifyAI API",
    lifespan=lifespan
)


# ---------------- CORS (Frontend Access) ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # later replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- Routers ----------------

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(recommend.router, prefix="/certs", tags=["Certifications"])
app.include_router(vault.router, tags=["Vault"])


# ---------------- Health Check ----------------

@app.get("/")
async def health_check():
    return {
        "status": "online",
        "database": "connected"
    }

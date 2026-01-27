from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.db import client
from routes import auth, recommend, vault
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on server start
    try:
        await client.admin.command("ping")
        print("✅ Backend connected to MongoDB Atlas")
    except Exception as e:
        print(f"❌ DB Connection Error: {e}")
    yield
    # Runs on server shutdown
    client.close()

# INITIALIZE ONLY ONCE
app = FastAPI(title="CertifyAI", lifespan=lifespan)

# 1. MIDDLEWARES
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

# 2. ROUTERS
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(recommend.router, prefix="/certs", tags=["Certifications"])
app.include_router(vault.router, prefix="/vault", tags=["Vault"])

# 3. HEALTH CHECK (Prevents the 404 at "/")
@app.get("/")
async def health_check():
    return {
        "status": "Certify AI Backend Online", 
        "version": "1.0.0",
    }
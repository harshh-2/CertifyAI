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


app = FastAPI(title="CertifyAI API", lifespan=lifespan)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(recommend.router, prefix="/certs", tags=["Certifications"])
app.include_router(vault.router, tags=["Vault"])   # 👈 vault routes

@app.get("/")
async def health_check():
    return {"status": "online", "database": "connected"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-session-key"
)

app.include_router(auth.router, prefix="/auth")
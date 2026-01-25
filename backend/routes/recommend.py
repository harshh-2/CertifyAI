from fastapi import APIRouter
from backend.config.db import cert_col
from backend.models.certification import Certification
from typing import List

router = APIRouter()

@router.get("/all", response_model=List[Certification])
async def get_all_certs():
    certs = []
    # 1. Pull everything from the cloud
    async for doc in cert_col.find({}):
        # 2. Map the ID (Mongo uses _id, Pydantic wants cert_id)
        if "_id" in doc:
            doc["cert_id"] = str(doc["_id"])
        
        # 3. Validate and clean using your Model
        try:
            clean_cert = Certification.model_validate(doc)
            certs.append(clean_cert)
        except Exception as e:
            print(f"⚠️ Skipping a broken record: {e}")
            
    # 4. Return to Frontend
    return certs
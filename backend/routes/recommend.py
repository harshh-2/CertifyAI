from fastapi import APIRouter, HTTPException
from backend.config.db import cert_col
from backend.models.certification import Certification
from bson import ObjectId
from typing import List

router = APIRouter()

@router.get("/all", response_model=List[Certification])
async def get_all_certs():
    certs = []
    async for doc in cert_col.find({}):
        certs.append(Certification.model_validate(doc))
    return certs
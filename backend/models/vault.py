from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VaultItem(BaseModel):
    title: str
    username: str
    password: str
    notes: Optional[str] = None
    created_at: datetime = datetime.utcnow()

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class Certification(BaseModel):
    # 'cert_id' from your JSON, but we use 'id' in Python
    id: str = Field(alias="cert_id")
    title: str
    provider: str
    domain: str
    difficulty: str
    duration_weeks: int
    price: float
    skills: List[str]
    rating: float

    model_config = ConfigDict(
        populate_by_name=True,  # Allows you to use either 'id' or 'cert_id'
        extra='ignore'          # Ignores MongoDB internal fields like __v
    )
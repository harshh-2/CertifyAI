from pydantic import BaseModel, Field, ConfigDict, AliasChoices
from typing import Optional, List, Any

class Certification(BaseModel):
    # This maps multiple possible database keys to your new clean schema
    Domain: Optional[Any] = Field(
        default="N/A", 
        validation_alias=AliasChoices("Domain", "domain")
    )
    Skill: Optional[Any] = Field(
        default="N/A", 
        validation_alias=AliasChoices("Skill", "skills")
    )
    Certification: Optional[Any] = Field(
        default="N/A", 
        validation_alias=AliasChoices("Certification", "name", "title")
    )
    Company: Optional[Any] = Field(
        default="N/A", 
        validation_alias=AliasChoices("Company", "provider")
    )

    model_config = ConfigDict(
        populate_by_name=True,
        extra='ignore' # This ignores the extra fields like 'rating' or 'price'
    )
from pydantic import BaseModel, Field
from typing import List

class EPPRule(BaseModel):
    id: int
    name: str = Field(..., description="Nombre del elemento de protección")
    required: bool = Field(..., description="Si es obligatorio en la zona")
    description: str

class EPPRulesResponse(BaseModel):
    rules: List[EPPRule]
from datetime import datetime
from typing import List, Optional

import uuid

from pydantic import BaseModel, UUID4, validator

class Inventory(BaseModel):
    inventory_id: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    brand_name: Optional[str]
    medicine_name: Optional[str]
    stock: Optional[float]
    dosage: float
    dosage_unit: int
    medication_type: int
    description: Optional[str]

    @validator('inventory_id', pre=True)
    def validate_inventory_id(cls, v):
        if not isinstance(v, str):
            if isinstance(v, uuid.UUID):
                return str(v)
        return v

    class Config:
        orm_mode = True

class UpsertInventory(BaseModel):
    user_id: str
    inventory: list[Inventory]
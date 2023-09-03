from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, UUID4


# Define schemas
class SymptomRequest(BaseModel):
    bodyPart: str   
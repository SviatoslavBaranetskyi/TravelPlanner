from pydantic import BaseModel
from typing import Optional

class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    visited: Optional[bool] = None

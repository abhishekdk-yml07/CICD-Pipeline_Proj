from pydantic import BaseModel
from typing import Optional

class HealthResponse(BaseModel):
    status: str
    version: str

class StatusResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float
    environment: str

class Item(BaseModel):
    # Removed id from here entirely
    name: str
    description: Optional[str] = None
    price: float

class ItemResponse(Item):
    id: int  # id is only required when sending data back to the user


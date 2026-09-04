from typing import Optional
from pydantic import BaseModel


class CourierModel(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = ""
    phone: Optional[str] = ""
from typing import Optional
from pydantic import BaseModel




class STaskAdd(BaseModel):
    title: str
    category: str
    description: Optional[str] = None


class STask(STaskAdd):
    id: int  
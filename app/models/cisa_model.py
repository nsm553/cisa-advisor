from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class Cisa(BaseModel):
    title: str
    description: str
    type: str 

class Advisory(BaseModel):
    title: str
    date: str
    advisory_id: str
    advisory_type: str
    affected_products: Optional[str]
    vendors: Optional[str]
    related_topics: Optional[str]
    summary: Optional[str]
    content: Optional[str]
    references: Optional[str]

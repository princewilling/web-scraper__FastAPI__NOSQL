from typing import Optional
from click import UUID
from pydantic import BaseModel


class ProductSchema(BaseModel):
    asin: str
    title: Optional[str]
    
class ProductScrapeEventSchema(BaseModel):
    uuid: UUID
    asin: str
    title: Optional[str]
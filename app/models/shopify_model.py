from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ShopifyProductVariant(BaseModel):
    id: int
    product_id: int
    title: str
    price: str
    sku: Optional[str] = None
    inventory_quantity: int

class ShopifyProduct(BaseModel):
    id: int
    title: str
    product_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    variants: List[ShopifyProductVariant]
    
class ShopifyOrder(BaseModel):
    id: int
    order_number: int
    customer: Optional[Dict[str, Any]] = None
    created_at: datetime
    total_price: str
    line_items: List[Dict[str, Any]]
    
class ShopifyDataResponse(BaseModel):
    products: Optional[List[ShopifyProduct]] = None
    orders: Optional[List[ShopifyOrder]] = None
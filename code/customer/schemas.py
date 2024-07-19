from ninja import Schema, ModelSchema, FilterSchema, Field
from datetime import datetime
from typing import Optional, List, Self
from pydantic import model_validator

from customer.models import Customer, Address,Metafield,Collect

class AddressIn(Schema):
    customer_id: int
    address1: str
    address2: Optional[str] = ''
    city: str
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''
    phone: Optional[str] = ''
    province: str
    country: str
    zip: str
    company: str
    name: Optional[str] = ''

class AddressOut(Schema):
    id: int
    customer_id: int
    first_name: str = Field(alias='customer.user.first_name')
    last_name: str = Field(alias='customer.user.last_name')
    company: str
    address1: str
    address2: str
    city: str
    province: str
    zip: str
    phone: Optional[str] = ''
    name: str
    default: bool

class AddressResp(Schema):
    customer_address: AddressOut

class CustomerIn(Schema):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    currency: Optional[str] = None

class CustomerOut(Schema):
    id: int
    email: str = Field(alias='user.email')
    created_at: datetime
    updated_at: datetime
    first_name: str = Field(alias='user.first_name')
    last_name: str = Field(alias='user.last_name')
    order_counts: int
    state: str
    verified_email: bool
    currency: str
    phone: str
    addresses: Optional[List[AddressOut]] = Field(alias='address_set')

class CustomerResp(Schema):
    customers: List[CustomerOut]

class MetafieldSchema(Schema):
    id: int
    created_at: datetime
    description: str
    key: str
    namespace: str
    owner_id: int
    owner_resource: str
    updated_at: datetime
    value: str
    type: str

    class Config:
        orm_mode = True

class MetafieldCreate(Schema):
    description: str
    key: str
    namespace: str
    owner_id: int
    owner_resource: str
    value: str
    type:str

class CollectOut(Schema):
    collection_id: int
    created_at: datetime
    collect_id : int
    position : str
    product_id: int
    sort_value : str
    updated_at : datetime
    
class CollectIn(Schema):
    collection_id: int
    collect_id : int
    position : str
    product_id: int
    sort_value : str
    
class CollectResp(Schema):
    customers: List[CollectOut]
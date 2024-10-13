from pydantic import BaseModel
from typing import List

class Entitlement(BaseModel):
    resource: str
    actions: List[str]  # e.g., ['read', 'write']

class User(BaseModel):
    user_id: str
    api_key: str
    entitlements: List[Entitlement]

class QueryRequest(BaseModel):
    sql_query: str
    api_key: str  # User's API Key

class QueryResponse(BaseModel):
    message: str
    status: str  # e.g., 'success' or 'error'
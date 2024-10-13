from fastapi import FastAPI, Depends, HTTPException
from .models import QueryRequest, QueryResponse
from .services import AuthService
from .utils import log_request

app = FastAPI()
auth_service = AuthService()

@app.post("/execute_query", response_model=QueryResponse)
def execute_query(query_request: QueryRequest):
    log_request(query_request.sql_query)

    # Authenticate user by API key
    user = auth_service.get_user_by_api_key(query_request.api_key)

    # Validate the query against user's entitlements
    try:
        auth_service.validate_query(user, query_request.sql_query)
    except HTTPException as e:
        return QueryResponse(message=e.detail, status="error")

    # If no issues, return success response (actual query execution logic can be added later)
    return QueryResponse(message="Query executed successfully", status="success")

from fastapi import FastAPI, HTTPException
from .models import AuthRequest, AuthResponse, RefreshTokenRequest
from .auth_service import AuthService

app = FastAPI()

auth_service = AuthService()

@app.post("/validate-query/", response_model=AuthResponse)
def validate_query(request: AuthRequest):
    """
    API to validate user permissions and entitlements based on API key.
    """
    try:
        auth_response = auth_service.validate_api_key(request)
        return auth_response
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/refresh-token/")
def refresh_token(request: RefreshTokenRequest):
    """
    API to refresh access token for a specific application.
    """
    try:
        result = auth_service.refresh_access_token(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to refresh access token.")

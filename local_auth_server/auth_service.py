import pymysql
from .cache import RedisCache
from .models import AuthRequest, AuthResponse, RefreshTokenRequest

class AuthService:
    def __init__(self):
        self.cache = RedisCache()
        self.mysql_conn = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            db='enterprise_auth_db'
        )

    def fetch_entitlements_from_db(self, api_key: str):
        # Query MySQL to get permissions and entitlements for the API key
        with self.mysql_conn.cursor() as cursor:
            sql = "SELECT entitlements, permission FROM user_auth WHERE api_key=%s"
            cursor.execute(sql, (api_key,))
            result = cursor.fetchone()
            if result:
                entitlements, permission = result
                return {"entitlements": entitlements.split(','), "permission": permission}
            return None

    def validate_api_key(self, request: AuthRequest) -> AuthResponse:
        # Check Redis cache first
        cached_data = self.cache.get_cached_data(request.api_key)
        if cached_data:
            # Return cached entitlements and permissions
            return AuthResponse(
                entitlements=cached_data['entitlements'],
                permission=cached_data['permission'],
                access_tokens={app: f"token_{app}" for app in request.applications}
            )

        # If not cached, check MySQL as the source of truth (SOT)
        entitlements_data = self.fetch_entitlements_from_db(request.api_key)
        if not entitlements_data:
            raise ValueError("UNAUTHORIZED: Invalid API Key")

        # Save to Redis cache
        self.cache.set_cached_data(request.api_key, entitlements_data)

        # Return response with entitlements, permissions, and access tokens
        return AuthResponse(
            entitlements=entitlements_data['entitlements'],
            permission=entitlements_data['permission'],
            access_tokens={app: f"token_{app}" for app in request.applications}
        )

    def refresh_access_token(self, request: RefreshTokenRequest):
        # Simulate calling the connector auth server to refresh the access token
        new_token = f"new_token_{request.application}"
        # In production, you'd use request.client_id and request.client_secret to refresh tokens
        return {"application": request.application, "access_token": new_token}

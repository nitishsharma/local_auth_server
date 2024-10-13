from fastapi import HTTPException
from .models import User, Entitlement, QueryRequest

class AuthService:
    def __init__(self):
        # Simulating a database with in-memory user data
        self.users_db = {
            "user123": User(
                user_id="user123",
                api_key="abc123",
                entitlements=[
                    Entitlement(resource="salesforce.contacts", actions=["read"]),
                    Entitlement(resource="zendesk.tickets", actions=["read", "write"])
                ]
            )
        }

    def get_user_by_api_key(self, api_key: str) -> User:
        for user in self.users_db.values():
            if user.api_key == api_key:
                return user
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    def validate_query(self, user: User, query: str) -> None:
        # Simulate checking the SQL query against user's entitlements
        # For simplicity, check if the query accesses resources the user has permission to.
        if "salesforce.contacts" in query and not any(e.resource == "salesforce.contacts" for e in user.entitlements):
            raise HTTPException(status_code=403, detail="MISSING_ENTITLEMENTS")
        # Further validation logic can be added here.
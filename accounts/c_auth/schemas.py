# people/schemas.py
from ninja import Schema, ModelSchema

from django.contrib.auth.models import Permission

from accounts.c_auth.models import CGroup
from accounts.companies.schemas import BranchModelSchema, CompanyModelSchema
from accounts.users.models.User import User
from accounts.users.models.UserProfile import UserProfile
from accounts.users.schemas import UserProfileModelSchema

# Schemas for validation
class TokenObtainPairIn(Schema):
    email: str
    password: str

class TokenObtainPairOut(Schema):
    access: str
    refresh: str

class TokenRefreshIn(Schema):
    refresh: str


# For the /me endpoint
class UserDetailsIn(Schema):
    access: str


class PermissionModelSchema(ModelSchema):
    class Meta:
        model = Permission
        fields: list[str] = ["name", "codename"]


class CGroupSchema(ModelSchema):
    name: str
    permissions: list[PermissionModelSchema]
    
    class Meta:
        model = CGroup
        fields: list[str] = ["name", "permissions"]


class UserDetailsOut(ModelSchema):
    c_groups: list[CGroupSchema]
    user_permissions: list[PermissionModelSchema]
    company: CompanyModelSchema
    accessible_branches: list[BranchModelSchema] = []
    profile: UserProfileModelSchema | None
    
    class Meta:
        model = User
        fields: list[str] = ["email", "is_company_admin", "company", "accessible_branches", "c_groups", "user_permissions"]
    
    @staticmethod
    def resolve_profile(obj: User) -> UserProfile | None:
        try:
            return obj.profile
        except Exception:
            return None

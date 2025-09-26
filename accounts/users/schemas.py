# people/schemas.py
from ninja import Schema, ModelSchema
from typing import List, Optional

from accounts.companies.schemas import BranchModelSchema, CompanyModelSchema
from .models.User import User
from .models.UserProfile import UserProfile


# Schemas for validation
class TokenObtainPairIn(Schema):
    email: str
    password: str


class TokenObtainPairOut(Schema):
    access: str
    refresh: str


class TokenRefreshIn(Schema):
    refresh: str


class UserProfileModelSchema(ModelSchema):
    class Meta:
        model = UserProfile
        fields: str = "__all__"

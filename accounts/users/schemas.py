# people/schemas.py
from ninja import Schema, ModelSchema
from typing import List, Optional

from accounts.companies.schemas import BranchModelSchema, CompanyModelSchema
from .models.User import User
from .models.UserProfile import UserProfile

class LoginSchema(Schema):
    email: str
    password: str

class UserProfileSchema(ModelSchema):
    class Meta:
        model = UserProfile
        fields = ["first_name", "middle_name", "last_name", "gender", "phone_1", "phone_2"]
 
class UserOutAuthedSchema(ModelSchema):
    company: CompanyModelSchema
    accessible_branches: List[BranchModelSchema] = []
    profile: UserProfileSchema = None

    class Meta:
        model = User
        fields = ["id", "email", "username", "company", "accessible_branches", "is_company_admin"]

    @staticmethod
    def resolve_company(obj):
        return obj.company

    @staticmethod
    def resolve_accessible_branches(obj):
        return obj.accessible_branches.all()

    @staticmethod
    def resolve_profile(obj):
        return obj.profile

class LoginResponseSchema(Schema):
    access: str
    user: UserOutAuthedSchema

# people/schemas.py
from ninja import Schema, ModelSchema
from typing import List, Optional
from .models.User import User
from .models.UserProfile import UserProfile

class LoginSchema(Schema):
    email: str
    password: str

class UserOut(Schema):
    id: int
    username: str
    email: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    company_id: Optional[int]
    company_name: Optional[str]
    branch_ids: List[int]
    branch_names: List[str]
    is_company_admin: bool

def _user_payload(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.profile.first_name,
        "middle_name": user.profile.middle_name,
        "last_name": user.profile.last_name,
        "company_id": user.profile.company.id if getattr(user, "company", None) else None,
        "company_name": user.profile.company.name if getattr(user, "company", None) else None,
        "branch_ids": [b.id for b in user.profile.accessible_branches.all()],
        "branch_names": [b.name for b in user.profile.accessible_branches.all()],
        "is_company_admin": getattr(user, "is_company_admin", False),
    }

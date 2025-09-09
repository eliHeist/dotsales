from ninja import Schema, ModelSchema
from typing import List, Optional

from .models import Company, Branch


class CompanyModelSchema(ModelSchema):
    class Meta:
        model = Company
        fields = ["id", "name", "address", "contact"]


class BranchModelSchema(ModelSchema):
    class Meta:
        model = Branch
        fields = ["id", "name", "location"]

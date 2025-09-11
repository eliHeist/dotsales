from django.urls import path
from . import views

app_name = "branches"

urlpatterns = [
    path("<int:bpk>", views.BranchesView.as_view(), name="landing"),
]
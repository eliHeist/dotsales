from django.urls import path
from . import views

app_name = "company"

urlpatterns = [
    path("", views.LandingPageView.as_view(), name="landing"),
    path("users/", views.UsersListView.as_view(), name="users"),
]
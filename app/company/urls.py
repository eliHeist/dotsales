from django.urls import path
from . import views

app_name = "company"

urlpatterns = [
    path("", views.LandingPageView.as_view(), name="landing"),
    path("branches/", views.BranchesPageView.as_view(), name="branches"),
    path("users/", views.UsersListView.as_view(), name="users"),
    path("products/", views.ProductListView.as_view(), name="products"),
]
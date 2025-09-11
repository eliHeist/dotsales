from django.urls import path
from .views import LandingPageView

app_name = "company"

urlpatterns = [
    path("", LandingPageView.as_view(), name="landing"),
]
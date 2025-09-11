from django.urls import path
from . import views

app_name = "branches"

urlpatterns = [
    path("<int:bpk>", views.BranchesView.as_view(), name="landing"),
    path("<int:bpk>/products", views.ProductsView.as_view(), name="products"),
    path("<int:bpk>/products/<int:pk>", views.ProductDetailView.as_view(), name="product-detail"),
]
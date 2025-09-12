from django.urls import path
from . import views

app_name = "branches"

urlpatterns = [
    path("<int:bpk>", views.BranchesView.as_view(), name="landing"),
    path("<int:bpk>/products", views.ProductsView.as_view(), name="products"),
    path("<int:bpk>/products/<int:pk>", views.ProductDetailView.as_view(), name="product-detail"),
    path("<int:bpk>/sales", views.SalesView.as_view(), name="sales"),
    path("<int:bpk>/sales/form", views.SalesFormView.as_view(), name="sales_form"),
    path("<int:bpk>/sales/form/<int:pk>", views.SalesFormView.as_view(), name="sales_form_update"),
]
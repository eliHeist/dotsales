from django.contrib import admin
from django.urls import path, include

from api.api import global_api

from .appsConfig import getAppUrls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", global_api.urls),
]

urlpatterns += getAppUrls()
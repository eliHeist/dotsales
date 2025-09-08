from django.contrib import admin
from django.urls import path, include

from api.api import api

from .appsConfig import getAppUrls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", api.urls),
]

urlpatterns += getAppUrls()
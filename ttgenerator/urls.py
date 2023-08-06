from django.contrib import admin
from django.urls import path, include  # new

urlpatterns = [
    path("", include("generator.urls"), name="generator"),
    path("admin/", admin.site.urls),
]

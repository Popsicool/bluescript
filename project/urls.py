from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('bluescript/', admin.site.urls),
    path("", include("app.urls"))
]

from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logout, name="logout"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("create", views.create_task, name="create"),
    path("edit/<str:id>", views.edit_task, name="edit"),
    path("completed/<str:id>", views.completed, name="completed"),
    path("delete/<str:id>", views.delete, name="delete"),
]

from django.conf.urls import handler404, handler500

handler404 = 'app.views.error_404_view'
handler500 = 'app.views.error_500_view'


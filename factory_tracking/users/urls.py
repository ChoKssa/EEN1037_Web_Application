from django.urls import path

from . import views
from api.views_web import api_key_management_view

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("api-keys/", api_key_management_view, name="manage_api_keys"),
    path("export-data/", views.export_data, name="export_data"),
    path("create-user/", views.create_user_or_edit, name="create_user_or_edit"),
    path("delete-user/", views.delete_user, name="delete_user"),
]

from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("api/process_data/", views.ProcessDataView.as_view(), name="process_data"),
    path("api/task_status/", views.ProcessStatusView.as_view(), name="task_status"),
    path("api/logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

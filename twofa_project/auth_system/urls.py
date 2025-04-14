from django.urls import path
from auth_system.views import register_page, login_page, home,login_request, login_verify, register, dashboard, logout_view

urlpatterns = [
    path("register/", register_page, name="register_page"),
    path("register-api/", register, name="register"),  
    path("login/", login_page, name="login_page"),
    path("login-request/", login_request, name="login_request"),
    path("login-verify/", login_verify, name="login_verify"),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", logout_view, name="logout"),
    path("", home, name="home"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("loans/", views.view_loans, name="view_loans"),
    path("logout/", views.logout_user, name="logout"),
]

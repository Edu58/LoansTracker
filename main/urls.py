from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile_update, name="profile_update"),
    path("loans/", views.view_loans, name="view_loans"),
    path("search-loans/", views.search_loans, name="search_loans"),
    path("analytics/", views.view_analytics, name="view_analytics"),
    path("logout/", views.logout_user, name="logout"),
]

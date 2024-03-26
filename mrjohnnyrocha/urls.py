# backend/mrjohnnyrocha/urls.py

from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

# Importing APIs
from app.apis import ForgotPasswordAPI, UserLoginAPI, UserSignupAPI, UserProfileAPI, WelcomePageAPI   

# Function for testing Sentry
def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include('rest_framework.urls', namespace='rest_framework')),
    path("api/", include('app.apis.urls', namespace='api')),  # Include app-specific URLs
    path('sentry-debug/', trigger_error),
    # Authentication and registration paths
    path("accounts/login/", UserLoginAPI.as_view(), name="login"),
    path("register/", UserSignupAPI.as_view(), name="register"),
    path("settings/", UserProfileAPI.as_view(), name="user_settings"),
    path("forgot-password/", ForgotPasswordAPI.as_view(), name="forgot_password"),
    # Password reset paths using Django's auth views
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    # Welcome page
    path("", WelcomePageAPI.as_view(), name="home"),
]

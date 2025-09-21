from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupView, VerifyView , ProfileView , ProfileUpdateView , ResetPasswordConfirmView , ResetPasswordRequestView

urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("verify/", VerifyView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("profile/update/", ProfileUpdateView.as_view()),
    path("password/reset/", ResetPasswordRequestView.as_view()),
    path("password/reset/confirm/", ResetPasswordConfirmView.as_view()),



]

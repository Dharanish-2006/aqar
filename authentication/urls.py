from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProfileView

urlpatterns = [
    path('auth/login/',    TokenObtainPairView.as_view()),
    path('auth/refresh/',  TokenRefreshView.as_view()),
    path('auth/profile/',  ProfileView.as_view()),
]
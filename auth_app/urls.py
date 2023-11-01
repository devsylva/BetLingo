from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

router = DefaultRouter()

urlpatterns = router.urls + [
    path("signup/", signUp, name="signup"),
    path("login/", MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name='logout'),
    path('change-password/', change_password, name='change_password'),
    path('update-user/', UserUpdateView.as_view(), name='update-user'),
]
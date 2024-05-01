from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
    TokenRefreshView,
    TokenBlacklistView
)

from users.views import (
    CreateUserView,
    ManageUserView,
    UserProfilesView
)

app_name = "users"

router = routers.DefaultRouter()
router.register("profiles", UserProfilesView, basename="profiles")

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("", include(router.urls)),
]

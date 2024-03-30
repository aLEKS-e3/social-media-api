from django.urls import path

from users.views import CreateUserView, CreateTokenView, ManageUserView

app_name = "users"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

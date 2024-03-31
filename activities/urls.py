from rest_framework import routers

from activities.views import PostViewSet


app_name = "activities"

router = routers.DefaultRouter()
router.register("posts", PostViewSet, basename="posts")

urlpatterns = router.urls

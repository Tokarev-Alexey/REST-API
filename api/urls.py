from rest_framework.routers import DefaultRouter
from posts.views import PostViewSet, CommentViewSet
from users.views import UserProfileViewSet, Podpiski

router = DefaultRouter()
router.register(r'post', PostViewSet, basename='post')
router.register(r'comment', CommentViewSet, basename='comment')
router.register(r'user', UserProfileViewSet, basename='user')
router.register(r'subscriptions', Podpiski, basename='subscriptions')
urlpatterns = router.urls

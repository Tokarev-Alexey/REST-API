from rest_framework.routers import DefaultRouter
from posts.views import PostViewSet, CommentViewSet
from users.views import UserProfileViewSet, Podpiski

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'users', UserProfileViewSet, basename='user')
router.register(r'subscriptions', Podpiski, basename='subscriptions')
urlpatterns = router.urls

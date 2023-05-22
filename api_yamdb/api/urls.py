from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ReviewsViewSet,
    CommentsViewSet,
    CategoryViewSet,
    GenreViewSet,
    TokenAPIView,
    SingUpAPIView,
    UserViewSet,
    TitleViewSet
)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', TokenAPIView.as_view(), name='get_token'),
    path('v1/auth/signup/', SingUpAPIView.as_view(), name='signup'),
]

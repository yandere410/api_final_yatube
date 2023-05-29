from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (PostViewSet, GroupViewSet,
                       CommentViewSet, FollowViewSet)


app_name = 'api'

router = DefaultRouter()
router.register(
    'posts', PostViewSet, basename='post')
router.register(
    'groups', GroupViewSet, basename='group')
router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment')
router.register('follows', FollowViewSet, basename='follow')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

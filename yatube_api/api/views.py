from rest_framework import viewsets, permissions, mixins, filters
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post, Group, Follow
from api.serializers import (
    PostSerializer, GroupsSerializer, CommentSerializer, FollowSerializer)
from api.permissions import IsAuthorOrReadOnly
from api.utils import get_post


class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """List view set for Follow"""
    pass


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for Posts"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly, ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Groups view set"""
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    pagination_class = LimitOffsetPagination


class CommentViewSet(viewsets.ModelViewSet):
    """Comment view set"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        return get_post(self.kwargs['post_id']).comments.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            post=get_post(self.kwargs['post_id'])
        )


class FollowViewSet(CreateListViewSet):
    """Follow view set"""
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'following__username']

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

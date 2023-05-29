from rest_framework import viewsets

from posts.models import Post, Group, Comment, Follow
from api.serializers import (
    PostSerializer, GroupsSerializer, CommentSerializer)
from api.permissions import IsAuthorOrReadOnly
from api.utils import get_post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            post=get_post(self.kwargs['post_id'])
        )

    def get_queryset(self):
        return get_post(self.kwargs['post_id']).comments.all()


class FollowViewSet(viewsets.ModelViewSet):
    ...

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Post, Group, Comment, Follow, User


class PostSerializer(serializers.ModelSerializer):
    """Post serializer"""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class GroupsSerializer(serializers.ModelSerializer):
    """Group serializer"""

    class Meta:
        fields = '__all__'
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """Follow serializer"""
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'

    )
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ['following', 'user']
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['following', 'user'])
        ]

    def validate(self, data):
        if data['following'] == self.context['request'].user:
            raise serializers.ValidationError('You can"t follow yourself')
        return data

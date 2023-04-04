from django.shortcuts import get_object_or_404
from rest_framework import permissions

from rest_framework import viewsets

from posts.models import Group, Post, Comment
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer,
                          GroupSerializer, PostSerializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [
        permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsAuthorOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.commens.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def perform_update(self, serializer):
        comment = get_object_or_404(Comment, id=self.kwargs.get('comment_id'))
        serialized = serializer(comment, data=self.request.data, partial=True)
        serialized.save()
        return get_object_or_404(Comment, id=self.kwargs.get('comment_id'))

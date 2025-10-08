import os

from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.utils import json

from project_config import settings
from project_config.create_token import create_token
from users.models import ProfileUser
from users.serializers import ProfileUserSerializer
from project_config.my_custom_permissions import IsOwnerOrReadOnly, IsOwnerCommentOrReadOnly


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = ProfileUser.objects.all()
    serializer_class = ProfileUserSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = ProfileUser.objects.get(username=request.data.get('username'))
        create_token(user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class Podpiski(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerCommentOrReadOnly]

    def list(self, request):
        return Response({'подписчики':'/subscribers/',
                         'подписки':'/subscriptions/',
                         'подписаться/отписаться':'/pk/subscription_on_or_off'})

    @action(detail=False, methods=['get'])
    def subscribers(self, request):
        authors = request.user.subscribers.all()
        serializer = ProfileUserSerializer(authors, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        subscriptions = request.user.subscriptions.all()
        serializer = ProfileUserSerializer(subscriptions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def subscription_on_or_off(self, request, pk=None):
        author = ProfileUser.objects.get(pk=pk)
        if author not in request.user.subscriptions.all():
            request.user.subscriptions.add(author)
            return Response(f'подписался')
        else:
            request.user.subscriptions.remove(author)
            return Response(f'отписался')

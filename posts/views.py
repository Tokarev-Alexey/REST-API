from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from project_config.my_custom_permissions import IsOwnerPostOrReadOnly, IsOwnerCommentOrReadOnly

from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-pub_date')
    serializer_class = PostSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerPostOrReadOnly]
    pagination_class = LimitOffsetPagination

    '''Для отображения имени автора (вместо ID) в API ответах используется ReadOnlyField в PostSerializer.
    Игнорирует любые попытки установить автора с POST запросом. Поскольку поле только для чтения, пользователь
    не может указать автора при создании поста, и на вход значение явно указанное пользовталем не приходит, 
    а для создания объекта поле нужно. Итак ради того, чтобы назначать имя автора по умолчанию, 
    необходимо было перед сохранением добавить имя текущего пользователя в данные сериализатора.'''

    def perform_create(self, serializer):
        # Данные после валидации: {'title': 'Пост', 'text': 'Текст'}
        serializer.save(author=self.request.user)# → {'title': 'Пост', 'text': 'Текст', 'author': user}

    @action(detail=False, methods=['get'])
    def posts_from_subscriptions(self, request):
        authors = request.user.subscriptions.all()
        posts = Post.objects.filter(author_id__in=authors).order_by('-pub_date')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-pub_date')
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerCommentOrReadOnly]
    pagination_class = LimitOffsetPagination
    '''Автоматом ставит юзера на место автора но к этому нужно еще чтобы поле author_comm=read_only в сериализаторе,
    иначе оно будет подставлено, но его все еще можно будет заменить'''
    def perform_create(self, serializer):
        serializer.save(author_comm=self.request.user)

    @action(detail=True, methods=['get'])
    def comments_from_post(self, pk=None):
        comments = Comment.objects.filter(post_id=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

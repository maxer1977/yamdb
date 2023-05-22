import uuid

from rest_framework import viewsets, filters, status, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from authorization.models import User
from reviews.models import Review, Category, Genre, Title
from .email import send_email_message
from .filters import BackendFilterTitle
from .permissions import (AuthorAdminModeratorOrReadOnly,
                          ReadOnly,
                          OnlyAdmin)
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          ReviewsSerializer,
                          CommentsSerializer,
                          SignUpSerializer,
                          TokenSerializer,
                          UserSerializer,
                          TitleListSerializer,
                          TitleSerializer)


class SingUpAPIView(APIView):
    """Регистрация пользователя."""

    queryset = User
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        if self.queryset.objects.filter(username=data.get('username'),
                                        email=data.get('email')).exists():
            return Response(data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        user = self.queryset.objects.get_or_create(
            username=data.get('username'),
            email=data.get('email'),
            confirmation_code=uuid.uuid4()
        )
        confirmation_code = user[0].confirmation_code
        email_body = (f'Привет! {data.get("username")}, '
                      f'Вы получили шанс попробовать наш сервис. Спасибо!\n'
                      f'Ваш код к API: {confirmation_code}')
        send_email_message(body=email_body, to=data.get('email'))
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAPIView(APIView):
    """Генерация токена."""

    queryset = User
    serializer_class = TokenSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = self.queryset.objects.get(
                username=serializer.validated_data.get('username')
            )
        except User.DoesNotExist:
            return Response({'username': 'Пользователя не существует!'},
                            status=status.HTTP_404_NOT_FOUND)
        if user.confirmation_code != serializer.validated_data.get(
                'confirmation_code'
        ):
            return Response(
                {'confirmation_code': 'Некорректный код'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для получения информации о пользователях."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [OnlyAdmin]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'username'
    search_fields = ['username']
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False,
            url_path='me',
            methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def user_me(self, request):
        if request.method == 'PATCH':
            serializer = self.serializer_class(request.user,
                                               data=request.data,
                                               partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BaseMixinsViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Базовый ViewSet."""

    filter_backends = [filters.SearchFilter]
    permission_classes = [OnlyAdmin | ReadOnly]
    search_fields = ['name']
    lookup_field = 'slug'


class CategoryViewSet(BaseMixinsViewSet):
    """ViewSet для категории произведений."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseMixinsViewSet):
    """ViewSet для жанра произведений."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """Управление функциями для работы с обзорами."""

    serializer_class = ReviewsSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        new_queryset = title.reviews.all()
        return new_queryset

    def create(self, request, *args, **kwargs):
        serializer = ReviewsSerializer(data=request.data)

        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)

        if not Review.objects.filter(
                author=self.request.user, title=title
        ).exists():
            serializer.is_valid(raise_exception=True)
            serializer.save(author=self.request.user, title=title)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response('Пользователь уже создал обзор к этой статье, '
                        'можно только отредактировать или удалить обзор',
                        status=status.HTTP_400_BAD_REQUEST)


class CommentsViewSet(viewsets.ModelViewSet):
    """Управление функциями для работы с обзорами."""

    serializer_class = CommentsSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""

    queryset = Title.objects.all()
    permission_classes = [OnlyAdmin | ReadOnly]
    filterset_class = BackendFilterTitle

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleListSerializer
        return TitleSerializer

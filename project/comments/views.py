from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Comment
from .serializers import CommentSerializer
from users.permissions import IsStaffOrReadOnly


class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all().select_related("article", "article__section")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]

    def perform_create(self, serializer):
        article_id = int(self.kwargs.get('article_pk'))
        author_id = self.request.user.amo_id  # Убедитесь, что это корректный способ получения идентификатора пользователя
        serializer.save(article_id=article_id, author_id=author_id)

    def get_queryset(self):
        user = self.request.user
        article_id = self.kwargs.get("article_pk")
        queryset = Comment.objects.filter(article_id=article_id).all().select_related("article", "article__section")
        if not user.is_staff:
            queryset = queryset.filter(article__section_id__in=user.view_list)
            print("User is not staff")
        return queryset
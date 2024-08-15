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
        article_id = self.kwargs.get('article_pk')
        author_id = self.request.user.amo_id  # Убедитесь, что это корректный способ получения идентификатора пользователя
        serializer.save(article_id=article_id, author_id=author_id)
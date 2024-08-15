from django.db import models
from articles.models import Article


class Comment(models.Model):
    author_id = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=280)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

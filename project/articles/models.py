from django.db import models


class Article(models.Model):
    name = models.CharField(max_length=255, blank=True, db_index=True)
    section = models.ForeignKey('sections.Section', on_delete=models.CASCADE, null=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    author = models.PositiveBigIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    content = models.TextField()
    position = models.PositiveIntegerField(default=0, db_index=True)

    def __str__(self):
        return self.name

from django.db import models



class Test(models.Model):
    article = models.ForeignKey("articles.Article", on_delete=models.CASCADE, unique=True)
    questions = models.JSONField(default=[])

    def __str__(self):
        return f"Test of {self.article.name}"
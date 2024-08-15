from django.contrib import admin
from django.urls import path, include
from sections.views import SectionViewSet
from articles.views import ArticleViewSet
from rest_framework import routers
from users.views import UserViewSet
from courses.views import CourseViewSet
from rest_framework_nested.routers import NestedSimpleRouter
from comments.views import CommentsViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"sections", SectionViewSet)
router.register(r"articles", ArticleViewSet)
router.register(r"users", UserViewSet)
router.register(r"courses", CourseViewSet)

articles_router = NestedSimpleRouter(router, r"articles", lookup="article")
articles_router.register(r"comments", CommentsViewSet, basename="article-comments")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api/v1/", include(articles_router.urls)),
]

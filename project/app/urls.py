from django.contrib import admin
from django.urls import path, include
from sections.views import SectionViewSet
from articles.views import ArticleViewSet
from rest_framework import routers
from users.views import UserViewSet
from courses.views import CourseViewSet
from rest_framework_nested.routers import NestedSimpleRouter
from comments.views import CommentsViewSet
from logs.views import LogEntryViewSet
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(AllowAny,),  # Разрешаем доступ всем для Swagger UI
    authentication_classes=[],  # Временно убираем кастомную аутентификацию
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"sections", SectionViewSet)
router.register(r"articles", ArticleViewSet)
router.register(r"users", UserViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"logs", LogEntryViewSet)

articles_router = NestedSimpleRouter(router, r"articles", lookup="article")
articles_router.register(r"comments", CommentsViewSet, basename="article-comments")

urlpatterns = [
    path("admin/", admin.site.urls),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("api/v1/", include(router.urls)),
    path("api/v1/", include(articles_router.urls)),
]

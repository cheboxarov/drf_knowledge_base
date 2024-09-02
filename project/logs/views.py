from rest_framework.viewsets import ModelViewSet
from .models import LogEntry
from .serializers import LogEntryListSerializer
from .permissions import IsStaff
from .pagination import StandardResultSetPagination


class LogEntryViewSet(ModelViewSet):
    queryset = LogEntry.objects.order_by("timestamp")
    serializer_class = LogEntryListSerializer
    permission_classes = [IsStaff]
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        return self.queryset.select_related("user").prefetch_related("content_object").all()
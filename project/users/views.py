from rest_framework.viewsets import ModelViewSet
from .models import User
from .permissions import UserEditPermissons
from .serializers import UserSerializer
from rest_framework.exceptions import NotFound


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserEditPermissons]
    lookup_field = "amo_id"

    # Переопределяет получение объекта при PATCH PUT на амовский id
    def get_queryset(self):
        return (
            User.objects.filter(project=self.request.user.project)
            .all()
            .select_related("project")
        )

    def get_object(self):
        amo_id = self.kwargs.get("amo_id")
        try:
            return User.objects.get(amo_id=amo_id)
        except User.DoesNotExist:
            raise NotFound("User with the specified amo_id does not exist.")

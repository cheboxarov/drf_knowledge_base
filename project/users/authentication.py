import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User
from django.db.models import Q
from projects.models import Project
from transliterate import translit


class CustomTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth = request.headers.get("Authorization")
        suburl = request.headers.get("Suburl")
        query = Project.objects.filter(suburl=suburl)
        if not query.exists():
            raise AuthenticationFailed("Project not found")
        project = query.first()
        if not project.is_active:
            raise AuthenticationFailed("Project has unactive status")
        if not auth:
            return None
        uuid = auth.split(" ")[1]
        try:
            filter = Q(amo_uuid=uuid)
            filter &= Q(last_sub_url=suburl)
            user = User.objects.filter(filter).first()
            if user:
                return (user, uuid)
        except:
            pass
        headers = {"Authorization": f"Bearer {project.amo_token}"}
        params = {"with": "uuid"}
        response = requests.get(
            f"https://{project.suburl}.amocrm.ru/api/v4/users",
            headers=headers,
            params=params,
        )
        if response.status_code != 200:
            raise AuthenticationFailed("Cant connect to project")
        try:
            users = response.json()["_embedded"]["users"]
            print(users)
            for user in users:
                if user["uuid"] == uuid:
                    user = self.get_user(user["id"], uuid, user["name"], project)
                    return (user, uuid)
        except:
            raise AuthenticationFailed("User not found")

    def get_user(self, user_id, user_uuid, username, project):
        try:
            user = User.objects.get(amo_id=user_id)
        except User.DoesNotExist:
            username = translit(
                username.replace(" ", "_"), language_code="ru", reversed=True
            )
            user = User.objects.create_user(
                amo_id=user_id,
                username=username,
                amo_uuid=user_uuid,
                last_sub_url=project.suburl,
                project=project,
            )

        return user

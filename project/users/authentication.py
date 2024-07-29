import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from users.models import User


class CustomTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth = request.headers.get("Authorization")
        if not auth:
            return None
        token = auth.split(" ")[1]
        try:
            user = User.objects.get(last_amo_token=token)
            if user:
                return (user, token)
        except :
            pass
        headers = {}
        headers["Authorization"] = auth
        response = requests.get("https://gktema.amocrm.ru/api/v4/leads",
                         headers=headers)

        decode = jwt.decode(token, options={'verify_signature': False})
        if response.status_code == 200:
            user = self.get_user(decode["sub"], token)
            return (user, token)
        else:
            raise AuthenticationFailed('Invalid token')


    def get_user(self, user_id, token):
        try:
            user = User.objects.get(amo_id=user_id)
            user.last_amo_token = token
            user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(amo_id=user_id, username=str(user_id), last_amo_token=token)
        return user

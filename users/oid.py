from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from users.models import CustomUser
from main.models import CustomGroup
from django.core.exceptions import ObjectDoesNotExist

class MITOIDCAB(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(MITOIDCAB, self).create_user(claims)

        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        try:
            group = CustomGroup.objects.get(name="tag@mit")
            group.members.add(sign_up)
            group.save()
        except ObjectDoesNotExist:
            pass
        user.save()

        return user

    def update_user(self, user, claims):
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.save()

        return user

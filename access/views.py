from django.http import JsonResponse

from .models import User


def authenticate_user(request, token: str):
    try:
        user = User.objects.get(token=token)
    except User.DoesNotExist:
        return JsonResponse(
            dict(success=False, payload=f'Not authenticated: Token "{token}" is not valid')
        )
    return JsonResponse(dict(success=True, payload=user.name))

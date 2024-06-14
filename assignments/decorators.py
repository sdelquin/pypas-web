from functools import wraps

from django.http import JsonResponse

from access.models import User


def auth_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            token = request.POST.get('token')
            User.objects.get(token=token)
        except User.DoesNotExist:
            return JsonResponse(
                dict(success=False, payload=f'Not authenticated: Token "{token}" is not valid')
            )
        return func(request, *args, **kwargs)

    return wrapper

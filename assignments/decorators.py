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
            msg = 'Token "{token}" is not valid' if token else 'Token must be defined'
            return JsonResponse(dict(success=False, payload=f'Authentication required: {msg}'))
        return func(request, *args, **kwargs)

    return wrapper

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import User


def authenticate_user(request, token: str):
    user = get_object_or_404(User, token=token)
    return JsonResponse(dict(name=user.name))

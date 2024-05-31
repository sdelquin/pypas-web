from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from access.models import User


@csrf_exempt
@require_POST
def stats(request):
    try:
        token = request.POST.get('token')
        user = User.objects.get(token=token)
    except User.DoesNotExist:
        return JsonResponse(
            dict(success=False, payload=f'Not authenticated: Token "{token}" is not valid')
        )

    return JsonResponse(
        dict(
            success=True,
            payload=dict(passed=user.num_passed_exercises, uploaded=user.num_uploaded_exercises),
        )
    )

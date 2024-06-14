from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from access.models import User
from exercises.models import Exercise

from .models import Assignment


@csrf_exempt
@require_POST
def upload(request, exercise_slug: str):
    try:
        exercise = Exercise.objects.get(slug=exercise_slug)
    except Exercise.DoesNotExist:
        return JsonResponse(
            dict(success=False, payload=f'Exercise "{exercise_slug}" does not exist')
        )
    try:
        token = request.POST.get('token')
        user = User.objects.get(token=token)
    except User.DoesNotExist:
        return JsonResponse(
            dict(success=False, payload=f'Not authenticated: Token "{token}" is not valid')
        )
    assignment, created = Assignment.objects.get_or_create(exercise=exercise, user=user)
    assignment.unzip(request.FILES.get('file'))
    assignment.passed = assignment.test()
    assignment.save()

    return JsonResponse(dict(success=True, payload=assignment.passed))


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

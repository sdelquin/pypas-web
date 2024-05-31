from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from access.models import User
from assignments.models import Assignment

from .models import Exercise


def get_exercise(request, slug: str):
    try:
        exercise = Exercise.objects.get(slug=slug)
    except Exercise.DoesNotExist:
        return JsonResponse(dict(success=False, payload=f'Exercise "{slug}" does not exist'))

    response = HttpResponse(exercise.zip(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={exercise.zipname}'
    return response


@csrf_exempt
@require_POST
def put_exercise(request, slug: str):
    try:
        exercise = Exercise.objects.get(slug=slug)
    except Exercise.DoesNotExist:
        return JsonResponse(dict(success=False, payload=f'Exercise "{slug}" does not exist'))
    try:
        token = request.POST.get('token')
        user = User.objects.get(token=token)
    except User.DoesNotExist:
        return JsonResponse(
            dict(success=False, payload=f'Not authenticated: Token "{token}" is not valid')
        )
    assignment, created = Assignment.objects.get_or_create(exercise=exercise, user=user)
    assignment.put(request.FILES.get('file'))
    assignment.passed = assignment.test()
    assignment.save()

    return JsonResponse(dict(success=True, payload=assignment.passed))

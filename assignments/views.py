from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from access.models import User
from chunks.models import Chunk
from exercises.models import Exercise

from .decorators import auth_required
from .models import Assignment


@auth_required
@csrf_exempt
@require_POST
def put(request, exercise_slug: str):
    user = User.objects.get(token=request.POST['token'])

    try:
        exercise = Exercise.objects.get(slug=exercise_slug)
    except Exercise.DoesNotExist:
        return JsonResponse(
            dict(success=False, payload=f'Exercise "{exercise_slug}" does not exist')
        )

    try:
        chunk = Chunk.objects.get(frame__context=user.context, exercise=exercise)
    except Chunk.DoesNotExist:
        return JsonResponse(
            dict(success=False, payload=f'Exercise "{exercise_slug}" is not available')
        )

    if not chunk.frame.is_active:
        return JsonResponse(
            dict(success=False, payload=f'Exercise "{exercise_slug}" is not active')
        )

    if not chunk.puttable:
        return JsonResponse(
            dict(success=False, payload=f'Exercise "{exercise_slug}" is not puttable')
        )

    assignment, created = Assignment.objects.get_or_create(chunk=chunk, user=user)
    assignment.remove_folder()
    assignment.unzip(request.FILES.get('file'))
    assignment.test()

    return JsonResponse(dict(success=True, payload=chunk.frame.bucket.name))


@auth_required
@csrf_exempt
@require_POST
def log(request):
    user = User.objects.get(token=request.POST['token'])
    frame = request.POST.get('frame')
    verbose = request.POST.get('verbose')
    payload = Assignment.log(user, frame, verbose)
    return JsonResponse(dict(success=True, payload=payload))

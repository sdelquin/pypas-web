from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from access.models import User
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

    # try:
    #     pack = Pack.objects.get(frame=Frame.get_active_frame(user.context), exercise=exercise)
    # except Pack.DoesNotExist:
    #     return JsonResponse(
    #         dict(
    #             success=False,
    #             payload=f'Exercise "{exercise_slug}" does not belong to the active frame',
    #         )
    #     )
    # else:
    #     if not pack.uploadable:
    #         return JsonResponse(
    #             dict(
    #                 success=False,
    #                 payload=f'Exercise "{exercise_slug}" is not uploadable for the active frame',
    #             )
    #         )

    assignment, created = Assignment.objects.get_or_create(exercise=exercise, user=user)
    assignment.remove_folder()
    assignment.unzip(request.FILES.get('file'))
    assignment.test()

    return JsonResponse(dict(success=True, payload='Exercise was successfully uploaded'))


@auth_required
@csrf_exempt
@require_POST
def log(request, verbose: bool = False):
    user = User.objects.get(token=request.POST['token'])
    return JsonResponse(dict(success=True, payload=Assignment.log(user, verbose)))

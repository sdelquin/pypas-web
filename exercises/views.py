import shutil
import zipfile

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from access.models import User

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

    upload_folder = user.get_exercise_folder(exercise)
    shutil.rmtree(upload_folder, ignore_errors=True)
    upload_folder.parent.mkdir(parents=True, exist_ok=True)
    file = request.FILES.get('file')
    with zipfile.ZipFile(file) as zip_ref:
        zip_ref.extractall(upload_folder)

    return JsonResponse(
        dict(success=True, payload=f'Good job {user}! Exercise has been successfully uploaded')
    )

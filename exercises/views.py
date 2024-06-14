from django.http import HttpResponse, JsonResponse

from .models import Exercise


def get(request, slug: str):
    try:
        exercise = Exercise.objects.get(slug=slug)
    except Exercise.DoesNotExist:
        return JsonResponse(dict(success=False, payload=f'Exercise "{slug}" does not exist'))

    response = HttpResponse(exercise.zip(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={exercise.zipname}'
    return response

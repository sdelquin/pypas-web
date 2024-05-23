from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Exercise


def get_exercise(request, slug: str):
    exercise = get_object_or_404(Exercise, slug=slug)
    response = HttpResponse(exercise.zip(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={exercise.zipname}'

    return response

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from access.models import Context, User

from .models import Exercise


@csrf_exempt
@require_POST
def get(request, slug: str):
    try:
        user = User.objects.get(token=request.POST.get('token'))
    except User.DoesNotExist:
        context = Context.objects.get(slug='public')
    else:
        context = user.context

    try:
        exercise = Exercise.objects.get(slug=slug)
    except Exercise.DoesNotExist:
        return JsonResponse(dict(success=False, payload=f'Exercise "{slug}" does not exist'))

    if chunk := context.get_chunk(exercise):
        if not chunk.frame.is_active:
            return JsonResponse(dict(success=False, payload=f'Exercise "{slug}" is not active'))
    else:
        return JsonResponse(dict(success=False, payload=f'Exercise "{slug}" is not available'))

    response = HttpResponse(exercise.zip(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={exercise.zipname}'
    return response


def list(request, topic: str = None):
    qs = Exercise.filter_by_topic(topic) if topic else Exercise.objects
    payload = [dict(slug=exercise.slug, topic=str(exercise.topic)) for exercise in qs]
    return JsonResponse(dict(success=True, payload=payload), safe=False)

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from access.models import Context, User
from exercises.models import Topic

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


@csrf_exempt
@require_POST
def list(request):
    try:
        user = User.objects.get(token=request.POST.get('token'))
    except User.DoesNotExist:
        context = Context.objects.get(slug='public')
    else:
        context = user.context

    primary_topic = request.POST.get('primary_topic')
    secondary_topic = request.POST.get('secondary_topic')

    qs = context.get_active_chunks()
    if any([primary_topic, secondary_topic]):
        topics_qs = Topic.filter_by_levels(primary_topic, secondary_topic)
        qs = qs.filter(exercise__topic__in=topics_qs)
    qs = qs.order_by('frame', 'exercise__topic', 'exercise')
    payload = [
        dict(frame=chunk.frame.name, exercise=chunk.exercise.slug, topic=str(chunk.exercise.topic))
        for chunk in qs
    ]
    return JsonResponse(dict(success=True, payload=payload), safe=False)

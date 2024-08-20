from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from access.models import Context, User
from chunks.models import Chunk

from .forms import ExerciseToFrameForm
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

    try:
        chunk = Chunk.objects.get(frame__context=context, exercise=exercise)
    except Chunk.DoesNotExist:
        return JsonResponse(dict(success=False, payload=f'Exercise "{slug}" is not available'))

    if not chunk.frame.is_active:
        return JsonResponse(dict(success=False, payload=f'Exercise "{slug}" is not active'))

    chunk.hits += 1
    chunk.save()

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

    frame = request.POST.get('frame')
    primary_topic = request.POST.get('primary_topic')
    secondary_topic = request.POST.get('secondary_topic')

    payload = Exercise.list(context, frame, primary_topic, secondary_topic)
    return JsonResponse(dict(success=True, payload=payload))


def add_exercises_to_frame(request):
    if request.method == 'POST':
        if (form := ExerciseToFrameForm(data=request.POST)).is_valid():
            exercise_ids = request.GET.get('exercise_ids').split(',')
            exercises = Exercise.objects.filter(pk__in=exercise_ids)
            frame = form.cleaned_data.get('frame')
            for exercise in exercises:
                Chunk.objects.get_or_create(frame=frame, exercise=exercise)
            messages.success(request, f'Exercises added successfully to {frame}')
            return redirect('admin:exercises_exercise_changelist')
    else:
        form = ExerciseToFrameForm()
    return render(
        request,
        'exercises/admin/add_exercises_to_frame.html',
        dict(form=form, title='Add exercises to frame'),
    )

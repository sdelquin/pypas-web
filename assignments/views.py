from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from access.models import User
from chunks.models import Chunk
from exercises.models import Exercise
from frames.models import Frame

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

    uploaded_file = request.FILES.get('file')
    assignment, created = Assignment.objects.get_or_create(chunk=chunk, user=user)
    assignment.remove_folder()
    assignment.unzip(uploaded_file)
    assignment.copy(uploaded_file)
    assignment.test()

    if assignment.chunk.pass_to_put:
        payload = f'Chunk {chunk.display} must pass the tests to be puttable. In case of failure, the assignment will be removed.'
    else:
        payload = f'Saved at frame: {chunk.frame}'

    return JsonResponse(dict(success=True, payload=payload))


@auth_required
@csrf_exempt
@require_POST
def log(request):
    user = User.objects.get(token=request.POST['token'])
    frame = request.POST.get('frame')
    verbose = request.POST.get('verbose')
    payload = Assignment.log(user, frame, verbose)
    return JsonResponse(dict(success=True, payload=payload))


@auth_required
@csrf_exempt
@require_POST
def pull(request, item_slug: str):
    user = User.objects.get(token=request.POST['token'])
    # Item can be either an exercise slug or a frame slug
    try:
        exercise = Exercise.objects.get(slug=item_slug)
        try:
            assignment = Assignment.objects.get(chunk__exercise=exercise, user=user)
        except Assignment.DoesNotExist:
            return JsonResponse(
                dict(success=False, payload=f'Assignment for exercise "{item_slug}" does not exist')
            )
        return FileResponse(
            open(assignment.zippath, 'rb'), as_attachment=True, filename=f'{item_slug}.zip'
        )
    except Exercise.DoesNotExist:
        try:
            frame = Frame.objects.get(bucket__slug=item_slug, context=user.context)
        except Frame.DoesNotExist:
            return JsonResponse(
                dict(
                    success=False, payload=f'Frame "{item_slug}" does not exist or is not available'
                )
            )
        frame_assignments = Assignment.zip_frame_assignments_for_user(frame, user)
        return FileResponse(
            open(frame_assignments, 'rb'), as_attachment=True, filename=f'{item_slug}.zip'
        )

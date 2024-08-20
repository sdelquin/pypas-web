from django.contrib import messages
from django.db.models.signals import post_save
from django.shortcuts import redirect, render

from shared.utils import DisabledSignal

from .forms import ChunkToFrameForm
from .models import Chunk
from .signals import fix_order_within_frame_post_save


def add_chunks_to_frame(request):
    if request.method == 'POST':
        if (form := ChunkToFrameForm(data=request.POST)).is_valid():
            chunk_ids = request.GET.get('chunk_ids').split(',')
            frame = form.cleaned_data.get('frame')
            order = Chunk.last_order(within_frame=frame) + 1
            with DisabledSignal(post_save, fix_order_within_frame_post_save, Chunk):
                for chunk_id in chunk_ids:
                    source_chunk = Chunk.objects.get(pk=chunk_id)
                    target_chunk, created = Chunk.objects.get_or_create(
                        frame=frame, exercise=source_chunk.exercise
                    )
                    if created:
                        target_chunk.order = order
                        target_chunk.save()
                        order += 1
            messages.success(request, f'Chunks added successfully to {frame}')
            return redirect('admin:chunks_chunk_changelist')
    else:
        form = ChunkToFrameForm()
    return render(
        request,
        'chunks/admin/add_chunks_to_frame.html',
        dict(form=form, title='Add chunks to frame'),
    )

from django import forms

from frames.models import Frame


class ChunkToFrameForm(forms.Form):
    frame = forms.ModelChoiceField(queryset=Frame.objects.all(), required=True)

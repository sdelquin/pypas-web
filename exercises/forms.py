from django import forms

from frames.models import Frame


class ExerciseToFrameForm(forms.Form):
    frame = forms.ModelChoiceField(queryset=Frame.objects.all(), required=True)

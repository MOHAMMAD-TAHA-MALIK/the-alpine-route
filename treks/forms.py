from django import forms
from .models import Trek, TrekEvent


class MultipleFileInput(forms.FileInput):
    """Custom FileInput that allows selecting multiple files without triggering Django's ValueError."""
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        if attrs:
            # Prevent passing 'multiple' directly inside attrs dict to super()
            attrs = attrs.copy()
            attrs.pop('multiple', None)
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        # Explicitly ensure the 'multiple' HTML attribute gets rendered on the tag
        if attrs is None:
            attrs = {}
        attrs['multiple'] = True
        return super().render(name, value, attrs, renderer)

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)


class TrekForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        required=False,
        help_text="Upload up to 3 images."
    )

    class Meta:
        model = Trek
        fields = ['title', 'destination', 'date', 'difficulty', 'max_participants']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Mont Blanc Circuit'}),
            'destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Chamonix, France'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class TrekEventForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        required=False,
        help_text="Upload up to 3 images."
    )

    class Meta:
        model = TrekEvent
        fields = ['title', 'destination', 'date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
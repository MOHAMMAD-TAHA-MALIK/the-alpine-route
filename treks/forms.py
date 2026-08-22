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


class MultipleFileField(forms.FileField):
    """
    FIX: forms.FileField.to_python() only knows how to handle a single
    UploadedFile. MultipleFileInput.value_from_datadict() returns a list
    (via files.getlist()), so as soon as 1+ files were selected, to_python()
    tried to read .name/.size off a list, hit an AttributeError, and Django
    reported that as the generic "No file was submitted. Check the encoding
    type on the form." error - even though enctype was set correctly all
    along. This overrides clean() to run the normal FileField validation on
    each file in the list individually instead of on the list as a whole.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = forms.FileField.clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(self, d, initial) for d in data]
        return single_file_clean(self, data, initial)


class TrekForm(forms.ModelForm):
    images = MultipleFileField(
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
    images = MultipleFileField(
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
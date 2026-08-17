from django import forms
from .models import Trek

class TrekForm(forms.ModelForm):
    class Meta:
        model = Trek
        fields = ['title', 'destination', 'date', 'difficulty']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
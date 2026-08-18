from django import forms

from .models import Trek, TrekEvent

class TrekEventForm(forms.ModelForm):
    class Meta:
        model = TrekEvent
        fields = ['title', 'description', 'date', 'location', 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class TrekForm(forms.ModelForm):
    class Meta:
        model = Trek
        fields = ['title', 'destination', 'date', 'difficulty']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
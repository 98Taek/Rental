from django import forms

from books.models import Rating


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='Search Books')


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1.0, 'max': 5.0, 'step': 0.1, 'class': 'form-control'}),
        }
